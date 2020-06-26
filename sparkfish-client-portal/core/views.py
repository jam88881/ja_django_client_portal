from django.http import HttpResponse
from django.shortcuts import render
from os import path
from .settings import TRELLO_API_KEY
from .settings import TRELLO_API_TOKEN
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
    statusData = [
    {
        "idx":"1",
        "week": "June 15-21",
        "reportHeader":"Here is the latest Status Report",
        "report":"""<ul>
                        <li>we did this</li>
                        <li>we did that</li>
                        <li>we got something done</li>
                    </ul>
                    <p><b>Percentage of authorized hours (x) for Month Year to date: (hours/x)%</b></p>
                    <p>If you have any questions or concerns about anything in this status report, please let us know.</p>
                    Regards,<br>
                    Sparkfish Team"""
    },
    {
        "idx":"2",
        "week": "June 8-14",
        "reportHeader":"Here is last week's Status Report",
                "report":"""<ul>
                        <li>we did this</li>
                        <li>we did that</li>
                        <li>we got something done</li>
                    </ul>
                    <p><b>Percentage of authorized hours (x) for Month Year to date: (hours/x)%</b></p>
                    <p>If you have any questions or concerns about anything in this status report, please let us know.</p>
                    Regards,<br>
                    Sparkfish Team"""
    },
    {
        "idx":"3",
        "week": "June 1-7",
        "reportHeader":"Status Report For June 1-7, 2020",
                "report":"""<ul>
                        <li>we did this</li>
                        <li>we did that</li>
                        <li>we got something done</li>
                    </ul>
                    <p><b>Percentage of authorized hours (x) for Month Year to date: (hours/x)%</b></p>
                    <p>If you have any questions or concerns about anything in this status report, please let us know.</p>
                    Regards,<br>
                    Sparkfish Team"""
    },
    {
        "idx":"4",
        "week": "May 25-31",
        "reportHeader":"Status Report For May 25-31, 2020",
                "report":"""<ul>
                        <li>we did this</li>
                        <li>we did that</li>
                        <li>we got something done</li>
                    </ul>
                    <p><b>Percentage of authorized hours (x) for Month Year to date: (hours/x)%</b></p>
                    <p>If you have any questions or concerns about anything in this status report, please let us know.</p>
                    Regards,<br>
                    Sparkfish Team"""
    }
    ]

    TmetricAPICAll(request)

    return render(request, 'status-reports.html', {'statusData':statusData, 'loggedHours':TmetricAPICAll(request)})

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

def TmetricAPICAll(request):
    #Sparkfish General Admin Board
    responseTrello = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN)
    trelloData = []
    statusReportsData = []
    finalStatusReportsData = []
    
    for i, elem in enumerate(responseTrello.json()):
        item = {"shortLink" : elem['shortLink'], "name" : elem['name'], "idShort" : elem['idShort']}
        trelloData.append(item)

    tmetricURL = "https://app.tmetric.com/api/accounts/18538/timeentries/132870" #?timeRange.startTime=2020-04-01T00:00:00Z&timeRange.endTime=2020-06-26T00:00:00Z"
    headers = { "Authorization" : 'Bearer 7ae182feb9c9ffa0a727d01584c62aced8829c72df528835d8ec68209887901a',
                "Content-Type" : "application/json"}
    responseTmetric = requests.get(tmetricURL, headers=headers)

    dateList = []
    dateListShift7 = []
    dNow = dt.datetime.now()
    td28Days = dt.timedelta(days = 28)
    dAMonthAgo = dNow - td28Days

    for i in lastFourSundays(dAMonthAgo.year, dAMonthAgo.month, dAMonthAgo.day):
        dateList.append(i)
    
    for i in lastFourSundays(dAMonthAgo.year, dAMonthAgo.month, dAMonthAgo.day,7):
        dateListShift7.append(i)

    for i, elemTmetric in enumerate(responseTmetric.json()):
        for j, elemTrello in enumerate(trelloData):
            try:
                if elemTrello['shortLink'] in elemTmetric['details']['projectTask']['relativeIssueUrl']:
                    ed = elemTmetric['endTime']
                    sd = elemTmetric['startTime']
                    dEndDate = dt.datetime(int(ed[:4]),int(ed[5:7]),int(ed[8:10]),int(ed[11:13]),int(ed[14:16]),int(ed[17:19]))
                    dStartDate = dt.datetime(int(sd[:4]),int(sd[5:7]),int(sd[8:10]),int(sd[11:13]),int(sd[14:16]),int(sd[17:19]))
                    item = {"duration" : str(dateDiff(dEndDate,dStartDate)), "idShort" : elemTrello['idShort'], "name" : elemTrello['name']}
                    statusReportsData.append(item)
            except:
                pass
                    
    shortIDList = []
    for elem in statusReportsData:
        if elem['idShort'] not in shortIDList:
            shortIDList.append(elem['idShort'])

    for idShort in shortIDList:
        sum = 0
        for elem in statusReportsData:
            if idShort == elem['idShort']:
                sum = sum + float(elem['duration'])
        finalStatusReportsData.append({"Name":elem['name'], "hours":(sum/3600)})
    return finalStatusReportsData
