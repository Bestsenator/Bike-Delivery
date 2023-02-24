from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    context = {
        'IndexMain': 'active',
    }
    return render(request, 'index/index.html', context)


def logout(request):
    redirectUrl = reverse('login-main')
    response = HttpResponseRedirect(redirectUrl)
    response.delete_cookie('Session')
    return response
