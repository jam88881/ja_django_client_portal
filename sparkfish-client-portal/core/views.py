from django.http import HttpResponse
from django.shortcuts import render
import requests
from datetime import date, timedelta

def dash(request):
    response = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key=4e15254bd0830e2b1f4e79d12bebf60d&token=6d46576c490239c0e0ba711c703b4daee24243e3485ab393381ba649a1f11272')

    boardData = response.json()

    #import pdb
    #pdb.set_trace()

    return render(request, 'dash.html', {'boardData':boardData})

def status(request):
    dateData = [
    {
        "week": "June 15-21",
    },
    {
        "week": "June 8-14",
    },
        {
        "week": "June 1-7",
    },
    {
        "week": "May 25-31",
    }
    ]

    return render(request, 'status-reports.html', {'dateData':dateData})
