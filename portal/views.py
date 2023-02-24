from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs import auth
from funcs.cookies import set_cookie
# Create your views here.


def index(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'DashboardActive': 'active',
        }
        return render(request, 'portal/index.html', context)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


