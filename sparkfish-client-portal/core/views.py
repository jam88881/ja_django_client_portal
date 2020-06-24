from django.http import HttpResponse
from django.shortcuts import render
from os import path
from .settings import TRELLO_API_KEY
from .settings import TRELLO_API_TOKEN
import os
import json
import requests
import yaml


def dash(request):
    response = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key='+ TRELLO_API_KEY +'&token=' + TRELLO_API_TOKEN)

    boradData = response.json()

    return render(request, 'dash.html', {'boradData':boradData})

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
    return render(request, 'status-reports.html', {'statusData':statusData})
