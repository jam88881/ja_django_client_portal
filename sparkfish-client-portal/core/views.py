from django.http import HttpResponse
from django.shortcuts import render
from os import path
from .settings import TRELLO_API_KEY
from .settings import TRELLO_API_TOKEN
from .settings import TMETRIC_TOKEN
import os
import json
import requests
import yaml
import datetime as dt
from datetime import timedelta
import pdb

def dash(request):
    response = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN)

    boardData = []
    for i, elem in enumerate(response.json()):
        item = {"idShort" : elem['idShort'], "name" : elem['name']}
        boardData.append(item)
        
    return render(request, 'dash.html', {'boardData':boardData})

def status(request):
    statusData = []

    response = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN)

    dateList = []
    dateListShift7 = []
    dNow = dt.datetime.now()
    td28Days = dt.timedelta(days = 28)
    dAMonthAgo = dNow - td28Days

    for i in lastFourSundays(dAMonthAgo.year, dAMonthAgo.month, dAMonthAgo.day):
        dateList.append(i)
    
    for i in lastFourSundays(dAMonthAgo.year, dAMonthAgo.month, dAMonthAgo.day,7):
        dateListShift7.append(i)

    dateList.reverse()
    dateListShift7.reverse()

    for i in range(1,5):

        if i == 1:
            header = "Here is the latest Status Report"
        elif i == 2:
            header = "Here is last week's Status Report"
        else:
            header = "Status report " + str(dateListShift7[i-1])
        TmetricAPIResponse = TmetricAPICall(request, response, dateList[i-1], dateListShift7[i-1])
        statusDataItem = {
            "idx":str(i),
            "week": str(dateList[i-1]) + " to " + str(dateListShift7[i-1]),
            "reportHeader":header,
            "report" : TmetricAPIResponse
        }
        statusData.append(statusDataItem)

    return render(request, 'status-reports.html', {'statusData':statusData, 'loggedHours':TmetricAPICall(request, response, dateList[0], dateListShift7[0]) })

def dateDiff(date1, date2):
    return (date1-date2).total_seconds()

def lastFourSundays(year, month, day, shift = 0):
    d = dt.date(year, month, day)
    if shift != 0:
        d += timedelta(days = 7)
    d += timedelta(days = 6 - d.weekday())
    for i in range(1,5):
        yield d
        d += timedelta(days = 7)

def TmetricAPICall(request, responseTrello, paramStartDate, paramEndDate):
    trelloData = []
    statusReportsData = []
    finalStatusReportsData = []
    
    for i, elem in enumerate(responseTrello.json()):
        item = {"shortLink" : elem['shortLink'], "name" : elem['name'], "idShort" : elem['idShort']}
        trelloData.append(item)

    tmetricURL = "https://app.tmetric.com/api/accounts/18538/timeentries/132870?timeRange.startTime=" + str(paramStartDate.year) + "-" + str(paramStartDate.month) + "-" + str(paramStartDate.day) + "T00:00:00Z&timeRange.endTime=" + str(paramEndDate.year) + "-" + str(paramEndDate.month) + "-" + str(paramEndDate.day) + "T23:59:59Z"
    headers = { "Authorization" : TMETRIC_TOKEN,
                "Content-Type" : "application/json"}
    responseTmetric = requests.get(tmetricURL, headers=headers)

    for i, elemTmetric in enumerate(responseTmetric.json()):
        for j, elemTrello in enumerate(trelloData):
            try:
                if elemTrello['shortLink'] in elemTmetric['details']['projectTask']['relativeIssueUrl']:
                    ed = elemTmetric['endTime']
                    sd = elemTmetric['startTime']
                    dEndDate = dt.datetime(int(ed[:4]),int(ed[5:7]),int(ed[8:10]),int(ed[11:13]),int(ed[14:16]),int(ed[17:19]))
                    dStartDate = dt.datetime(int(sd[:4]),int(sd[5:7]),int(sd[8:10]),int(sd[11:13]),int(sd[14:16]),int(sd[17:19]))
                    item = {"duration" : str(dateDiff(dEndDate,dStartDate)), "idShort" : elemTrello['idShort'], "name" : elemTmetric['details']['projectTask']['description']}
                    statusReportsData.append(item)
            except:
                pass

    shortTaskList = []
    for elem in statusReportsData:
        if elem['idShort'] not in shortTaskList:
            shortTaskList.append(elem['idShort'])

    for taskID in shortTaskList:
        sum = 0
        for elem in statusReportsData:
            if taskID == elem['idShort']:
                sum = sum + float(elem['duration'])
                taskName = elem['name']
        finalStatusReportsData.append({"id":taskID, "name":taskName, "hours": str(round((sum/3600), 2)) })

    return finalStatusReportsData
