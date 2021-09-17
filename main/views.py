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
        print(request)
        return HttpResponseRedirect(f'https://www.facebook.com/v11.0/dialog/oauth?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&state={"{st=state123abc,ds=123456789}&scope=email,public_profile"}')
    else:
        print(request)
        req = urlparse(request.get_full_path_info())
        req = req.query.split('&')
        req = req[0].replace('code=','')

        access_token = requests.get(f'https://graph.facebook.com/v11.0/oauth/access_token?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&client_secret={app_secret}&code={req}')
        access_token = access_token.json()
        access_token = access_token.get("access_token")
        # print(f"The access token is {access_token}")
    
        app_access_token = requests.get(f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials")
        app_access_token = app_access_token.json()
        # print(app_access_token)
        app_access_token = app_access_token.get("access_token")
        # print('This is the app access token',app_access_token,'\n')

        check = requests.get(f'https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_access_token}')
        user_id = check.json()
        user_id = user_id.get("data")["user_id"]
        # print(user_id)
        profile = requests.get(f'https://graph.facebook.com/{user_id}?fields=id,name,email,picture&access_token={access_token}&client_secret={app_secret}&client_id={app_id}')
        print(profile.json())
        return HttpResponse('done')
