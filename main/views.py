from django.contrib.auth.decorators import login_required
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
from .backends import UserBackend
from django.contrib.auth import login
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView
from .decorators import login_excluded
Backend = UserBackend()
from django.conf import settings
import uuid

# from urllib.request import urlopen

@login_required()
def home(request):
    user = request.user
    user_id = user.user_id
    data = User.objects.filter(user_id=user_id)
    # media_base_dir = {settings.MEDIA_ROOT}
    # print(media_base_dir)
    for person in data:
        print(person.image)
    dict = {'user_id':user_id,
            'data':data}
    return render(request, 'main/app.html', dict)

@login_excluded('home')
def login_normal(request):
    # next = request.GET.get('next', None)
    # print('the result: ',next)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email,password)
            user = Backend.authenticate(request,email=email, password=password)
            # print(user.is_authenticated)
            if user.is_authenticated == True:
                login(request, user)
                return redirect(home)
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_excluded('home')
def login_facebook(request):  
    app_id = config('app-id')
    app_secret = config('app-secret')
    if (request.get_full_path_info() == "/login_facebook/"):
        return HttpResponseRedirect(f'https://www.facebook.com/v11.0/dialog/oauth?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&state={"{st=state123abc,ds=123456789}&scope=email"}')
    else:
        req = request.GET.get('code')
        access_token = requests.get(f'https://graph.facebook.com/v11.0/oauth/access_token?client_id={app_id}&redirect_uri=http://localhost:8000/login_facebook/&client_secret={app_secret}&code={req}')
        access_token = access_token.json().get("access_token")
        print(access_token)
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
            picture_name = f'profiles/facebook/{user_id}.jpg'
            picture.raw.decode_content = True

            with open(f'{settings.MEDIA_ROOT}/{picture_name}', 'wb') as f:
                shutil.copyfileobj(picture.raw, f)

            defaults['image'] = picture_name

        User.objects.update_or_create(user_id=user_id, defaults=defaults)
        user = Backend.get_user(user_id)
        print(user)
        login(request, user)
        
    return redirect('home')


@login_excluded('home')
def signup(request):
    # next = request.GET.get('next', None)
    # print('the result: ',next)
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            image = form.cleaned_data['image']
            user_id = uuid.uuid4()
            if not image is None:
                image.name = f'{user_id}.jpg'



            # left here


            if password != confirm_password:
                form.add_error(None, 'password mismatched')
                form.non_field_errors()
                print(form.non_field_errors())
                
            user = User.objects.create_user(email,password, name=name, image=image, user_id=user_id)
            return HttpResponse('success')
            
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
    