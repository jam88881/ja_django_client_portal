from django.http import HttpResponse
from django.shortcuts import render
import requests

def dash(request):
    response = requests.get('')

    boradData = response.json()

    return render(request, 'dash.html', {'boradData':boradData})
