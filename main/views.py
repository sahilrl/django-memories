from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

def home(request):
    return render(request, 'main/index.html')


def login_facebook(request):
    response = redirect('https://www.facebook.com/v11.0/dialog/oauth?client_id=365167805111881&redirect_uri=http://localhost:8000&state={"{st=state123abc,ds=123456789}"}')
    print(response)
    return response
