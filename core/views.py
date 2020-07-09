import datetime as dt
import json
import os
import requests
import yaml
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render

from os import path
from .settings import TRELLO_API_KEY, TRELLO_ACCOUNT_ID, TRELLO_USER_PROFILE_ID, TRELLO_API_TOKEN, TMETRIC_TOKEN

headers = { "Authorization" : TMETRIC_TOKEN, "Content-Type" : "application/json"}

def dash(request):
    board_data = []
    for e in request.user.user_permissions.filter(content_type = 13): #13 is trelloaccess
        trello_api_url = 'https://api.trello.com/1/boards/' + e.codename + '/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN
        response = requests.get(trello_api_url)

        for i, elem in enumerate(response.json()):
            item = {"id" : elem['idShort'], "name" : elem['name']}
            board_data.append(item)

    return render(request, 'dash.html', {'board_data':board_data})

def last_four_sundays(year, month, day, shift = 0):
    d = dt.date(year, month, day)
    if shift != 0:
        d += timedelta(days = 7)
    d += timedelta(days = 6 - d.weekday())
    for i in range(1,5):
        yield d
        d += timedelta(days = 7)

def status(request):

    status_data = []
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
    for e in request.user.user_permissions.filter(content_type = 13):
        board_name = str(e).split('|')[2].replace('_',' ').replace(' Access','')
        for i in range(1,5):

            if i == 1:
                header = "Here is the latest Status Report"
            elif i == 2:
                header = "Here is last week's Status Report"
            else:
                header = "Status report " + str(date_list_shift_7[i-1])

            status_data_item = {
                "idx" : str(i),
                "week" : str(date_list[i-1]) + " to " + str(date_list_shift_7[i-1]),
                "report_header" : header,
                "report" : get_board_related_tmetric_entries(e.codename, date_list[i-1], date_list_shift_7[i-1])
            }
            status_data.append(status_data_item)

    return render(request, 'status-reports.html', {'status_data':status_data, 'board_name':board_name})


def get_trello_cards(board):
    trello_card_data = []
    trello_cards_url = 'https://api.trello.com/1/boards/' + board + '/cards/?key=' + TRELLO_API_KEY + '&token=' + TRELLO_API_TOKEN
    trello_cards_response_json = requests.get(trello_cards_url).json()
    for elem_trello_card in trello_cards_response_json:
        trello_card_data.append({'idShort':elem_trello_card['idShort'],
                                 'shortLink':elem_trello_card['shortLink'],
                                 'name':elem_trello_card['name']})
    return trello_card_data


def get_tmetric_user_profile_ids():
    user_profile_id_data = []
    user_profile_id_request_url = 'https://app.tmetric.com/api/accounts/18538/timeentries/group'
    user_profile_id_response_json = requests.get(user_profile_id_request_url, headers=headers).json()
    for elem_user_profile_id in user_profile_id_response_json:
        user_profile_id_data.append({'userProfileID':str(elem_user_profile_id['userProfileId'])})
    return user_profile_id_data


def get_tmetric_entries(user_profile_id, param_start_date, param_end_date):
    loop_count = 0
    budget = 'No budget'
    entries_data = []
    entries_data_request_url = 'https://app.tmetric.com/api/accounts/18538/timeentries/'+ user_profile_id +"?timeRange.startTime=" + str(param_start_date.year) + "-" + str(param_start_date.month) + "-" + str(param_start_date.day) + "T00:00:00Z&timeRange.endTime=" + str(param_end_date.year) + "-" + str(param_end_date.month) + "-" + str(param_end_date.day) + "T23:59:59Z"
    entries_data_response_json = requests.get(entries_data_request_url, headers=headers).json()
    for elem_entries_data in entries_data_response_json:
        #try to get the board budget

        if loop_count == 0:
            try:
                budget = get_project_budget(elem_entries_data['details']['projectId'])
            except:
                pass
        try:
            end_time = elem_entries_data['endTime']
            start_time = elem_entries_data['startTime']
            end_date = dt.datetime(int(end_time[:4]),int(end_time[5:7]),int(end_time[8:10]),int(end_time[11:13]),int(end_time[14:16]),int(end_time[17:19]))
            start_date = dt.datetime(int(start_time[:4]),int(start_time[5:7]),int(start_time[8:10]),int(start_time[11:13]),int(start_time[14:16]),int(start_time[17:19]))
            entries_data.append({'relativeIssueID':elem_entries_data['details']['projectTask']['relativeIssueUrl'], 'duration':(end_date-start_date).total_seconds()})
        except:
            pass
        loop_count += 1
    return entries_data, budget


def get_project_budget(project_id):
    budget_url = 'https://app.tmetric.com/api/accounts/18538/projects/' + str(project_id)
    response = requests.get(budget_url, headers=headers)
    try:
        return response.json()['budgetSize']
    except:
        return 'No budget'


def get_board_related_tmetric_entries(board, start_date, end_date):
    master_budget = 'No budget'
    all_tmetric_entries = []
    tmetric_user_profile_ids = get_tmetric_user_profile_ids()
    for i in tmetric_user_profile_ids:
        tmetric_entries, board_budget = get_tmetric_entries(i['userProfileID'], start_date, end_date)
        #save a budget value if it is found, don't bother if it has already been found
        if board_budget != 'No budget' and master_budget == 'No budget':
            master_budget = board_budget
        for j in tmetric_entries:
            all_tmetric_entries.append(j)

    #sum up tmetric entries based on what is in the boards
    #project_id = ''
    board_related_tmetric_entries = []
    trello_cards = get_trello_cards(board)
    for card in trello_cards:
        hours_sum = 0
        for entry in all_tmetric_entries:
            if card['shortLink'] in entry['relativeIssueID']:
                hours_sum = hours_sum + float(entry['duration'])
                #project_id = entry['details']['projectID']
        if hours_sum > 0:
            board_related_tmetric_entries.append({'id':card['idShort'],'name':card['name'],'hours':round(((hours_sum/60)/60),2),'budget':str(master_budget)})

    return board_related_tmetric_entries

