from typing import get_type_hints
from django.http import response
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from urllib.parse import urlparse
from decouple import config
import requests

i = 0

def home(request):
    return render(request, 'main/index.html')


def login_facebook(request):
    app_id = config('app-id')
    app_secret = config('app-secret')
    if (request.get_full_path_info() == "/login_facebook/"):
        return HttpResponseRedirect('https://www.facebook.com/v11.0/dialog/oauth?client_id=365167805111881&redirect_uri=http://localhost:8000/login_facebook/&state={"{st=state123abc,ds=123456789}"}')
    else:
        req = urlparse(request.get_full_path_info())
        req = req.query.split('&')
        req = req[0].replace('code=','')
        access = requests.get(f'https://graph.facebook.com/v11.0/oauth/access_token?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&client_secret={app_secret}&code={req}')
        print('THis is another one ', access.json())
        return HttpResponse('done')
