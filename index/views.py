from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs import checker
# Create your views here.


def index(request):
    context = {
        'IndexMain': 'active',
    }
    if checker.mobile(request) is True:
        context['isMobile'] = True
    return render(request, 'index/index.html', context)


def logout(request):
    redirectUrl = reverse('login-main')
    response = HttpResponseRedirect(redirectUrl)
    response.delete_cookie('Session')
    return response
