# from django.shortcuts import render
# from functools import wraps


# def login_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         try:
#             user_id = request.session['login_status']
#         except:
#             return render(request, 'main/login.html')
#         return view_func(request, user_id)
#     return wrapper


from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User

class FacebookBackend(BaseBackend):

    def authenticate(self, request, email=None, access_token=None):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
            try:
                return User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return None