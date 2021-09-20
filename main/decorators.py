from django.shortcuts import render
from functools import wraps
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.session['login_status']
        except:
            return render(request, 'main/login.html')
        return view_func(request, user_id)
    return wrapper
