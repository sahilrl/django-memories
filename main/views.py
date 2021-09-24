from .decorators import login_required
from types import FrameType
from typing import get_type_hints
from django.db.models.fields import EmailField
from django.http import response
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from urllib.parse import urlparse
from decouple import config
import requests
from .models import User
import shutil # to save image on computer
from django.conf import settings
# from urllib.request import urlopen

@login_required
def home(request, user_id):
    data = User.objects.filter(user_id=user_id)
    dict = {'user_id':user_id,
            'data':data}
    return render(request, 'main/app.html', dict)


def login_facebook(request):  
    app_id = config('app-id')
    app_secret = config('app-secret')
    if (request.get_full_path_info() == "/login_facebook/"):
        return HttpResponseRedirect(f'https://www.facebook.com/v11.0/dialog/oauth?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&state={"{st=state123abc,ds=123456789}&scope=email"}')
    else:
        req = urlparse(request.get_full_path_info())
        req = req.query.split('&')
        req = req[0].replace('code=','')
        access_token = requests.get(f'https://graph.facebook.com/v11.0/oauth/access_token?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&client_secret={app_secret}&code={req}')
        access_token = access_token.json().get("access_token")
        app_access_token = requests.get(f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials")
        app_access_token = app_access_token.json().get("access_token")
        check = requests.get(f'https://graph.facebook.com/debug_token?input_token={access_token}&access_token={app_access_token}')
        user_id = check.json().get("data")["user_id"]
        profile = requests.get(f'https://graph.facebook.com/{user_id}?fields=id,name,email,picture.width(400).height(400)&access_token={access_token}&client_secret={app_secret}&client_id={app_id}')
        profile = profile.json()
        name, email, picture_url = profile['name'], profile['email'], profile['picture'].get('data')['url']
        # Getting profile picture
        picture = requests.get(picture_url, stream = True )

        defaults={'name':name, 'email':email, 'access_token':access_token, 'user_id':user_id}
        if picture.status_code == 200:
            picture_name = f'main/profiles/{user_id}.jpg'
            picture.raw.decode_content = True

            with open(f'{settings.BASE_DIR}/main/static/{picture_name}', 'wb') as f:
                shutil.copyfileobj(picture.raw, f)

            defaults['image'] = picture_name

        User.objects.update_or_create(user_id=user_id, defaults=defaults)
        request.session['login_status'] = user_id
    return redirect('home')
