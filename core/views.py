import datetime as dt
import json
import os
import requests
import yaml
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render

from os import path
from .settings import TRELLO_API_KEY, TRELLO_API_TOKEN, TMETRIC_TOKEN, TRELLO_API_TOKEN, TMETRIC_TOKEN


def dash(request):
    board_data = []
    for e in request.user.user_permissions.filter(content_type = 13): #13 is trelloaccess
        trello_api_url = 'https://api.trello.com/1/boards/' + e.codename + '/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN
        response = requests.get(trello_api_url)

        for i, elem in enumerate(response.json()):
            item = {"id" : elem['idShort'], "name" : elem['name']}
            board_data.append(item)

    return render(request, 'dash.html', {'board_data':board_data})

def status(request):
    for e in request.user.user_permissions.filter(content_type = 13): #13 is trelloaccess
        trello_api_url = 'https://api.trello.com/1/boards/' + e.codename + '/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN

    board_name = str(e).split('|')[2].replace('_',' ').replace(' Access','')

    status_data = []
    response = requests.get(trello_api_url)

    date_list = []
    date_list_shift_7 = []
    now = dt.datetime.now()
    time_delta_28_days = dt.timedelta(days = 28)
    a_month_ago = now - time_delta_28_days

    for i in last_four_sundays(a_month_ago.year, a_month_ago.month, a_month_ago.day):
        date_list.append(i)
    
    for i in last_four_sundays(a_month_ago.year, a_month_ago.month, a_month_ago.day,7):
        date_list_shift_7.append(i)

    date_list.reverse()
    date_list_shift_7.reverse()

    for i in range(1,5):

        if i == 1:
            header = "Here is the latest Status Report"
        elif i == 2:
            header = "Here is last week's Status Report"
        else:
            header = "Status report " + str(date_list_shift_7[i-1])
        tmetric_entries = get_tmetric_entries(request, response, date_list[i-1], date_list_shift_7[i-1])
        status_data_item = {
            "idx":str(i),
            "week": str(date_list[i-1]) + " to " + str(date_list_shift_7[i-1]),
            "report_header":header,
            "report" : tmetric_entries
        }

        status_data.append(status_data_item)

    return render(request, 'status-reports.html', {'status_data':status_data, 'board_name':board_name})

def dateDiff(date1, date2):
    return (date1-date2).total_seconds()

def last_four_sundays(year, month, day, shift = 0):
    d = dt.date(year, month, day)
    if shift != 0:
        d += timedelta(days = 7)
    d += timedelta(days = 6 - d.weekday())
    for i in range(1,5):
        yield d
        d += timedelta(days = 7)

def get_project_budget(project_id):
    budget_url = 'https://app.tmetric.com/api/accounts/18538/projects/' + str(project_id)
    headers = { "Authorization" : TMETRIC_TOKEN,
                "Content-Type" : "application/json"}
    response = requests.get(budget_url, headers=headers)
    try:
        return response.json()['budgetSize']
    except:
        return 'No Budget'

def get_tmetric_entries(request, trello_response, start_date, end_date):
    trello_data = []
    status_reports_data = []
    final_status_report_data = []
    project_id = ''
    headers = { "Authorization" : TMETRIC_TOKEN,"Content-Type" : "application/json"}

    for elem in trello_response.json():
        item = {"shortLink" : elem['shortLink'], "name" : elem['name'], "idShort" : elem['idShort']}
        trello_data.append(item)

    headers = { "Authorization" : TMETRIC_TOKEN,"Content-Type" : "application/json"}

    profile_id_url = 'https://app.tmetric.com/api/accounts/18538/timeentries/group'
    profile_id_data = requests.get('https://app.tmetric.com/api/accounts/18538/timeentries/group', headers=headers).json()

    for elem_profile_id in profile_id_data:
        tmetric_url = "https://app.tmetric.com/api/accounts/18538/timeentries/"+ str(elem_profile_id['userProfileId']) +"?timeRange.startTime=" + str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day) + "T00:00:00Z&timeRange.endTime=" + str(end_date.year) + "-" + str(end_date.month) + "-" + str(end_date.day) + "T23:59:59Z"
        response_tmetric = requests.get(tmetric_url, headers=headers)

        for elem_tmetric in response_tmetric.json():
            for elem_trello in trello_data:
                try:
                    if elem_trello['shortLink'] in elem_tmetric['details']['projectTask']['relativeIssueUrl']:
                        end_time = elem_tmetric['endTime']
                        start_time = elem_tmetric['startTime']
                        end_date = dt.datetime(int(end_time[:4]),int(end_time[5:7]),int(end_time[8:10]),int(end_time[11:13]),int(end_time[14:16]),int(end_time[17:19]))
                        start_date = dt.datetime(int(start_time[:4]),int(start_time[5:7]),int(start_time[8:10]),int(start_time[11:13]),int(start_time[14:16]),int(start_time[17:19]))
                        item = {"duration" : str(dateDiff(end_date,start_date)), "idShort" : elem_trello['idShort'], "name" : elem_tmetric['details']['projectTask']['description']}
                        status_reports_data.append(item)
                        project_id = elem_tmetric['details']['projectId']
                except:
                    pass
                    
        short_task_list = []
        for elem in status_reports_data:
            if elem['idShort'] not in short_task_list:
                short_task_list.append(elem['idShort'])

        for task_id in short_task_list:
            hours_sum = 0
            for elem in status_reports_data:
                if task_id == elem['idShort']:
                    hours_sum = hours_sum + float(elem['duration'])
                    task_name = elem['name']
        try:
            if len(task_name) > 0:
                final_status_report_data.append({"id":task_id, "name":task_name, "hours": str(round((hours_sum/3600), 2)), "budget": str(get_project_budget(project_id)) })
                task_name = ''
        except:
            pass
        status_reports_data = []


    return final_status_report_data
