from django.http import HttpResponse
from django.shortcuts import render
import requests

def dash(request):
    response = requests.get('https://api.trello.com/1/boards/B5t1aUPH/cards/?key=4e15254bd0830e2b1f4e79d12bebf60d&token=6d46576c490239c0e0ba711c703b4daee24243e3485ab393381ba649a1f11272')

    boradData = response.json()

    return render(request, 'dash.html', {'boradData':boradData})
