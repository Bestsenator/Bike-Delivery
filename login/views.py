from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs import auth
from signup.models import Customer, Courier, BikeDeliveryManger
from funcs.cookies import set_cookie

# Create your views here.


def index(request):
    context = {}
    if request.COOKIES.get('Notif401'):  # from portal --> session not found or expired
        context = {
            'SessionExpired': True,
        }
    return render(request, 'login/index.html', context)


def check(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        redirectUrl = reverse('portal-main')
        return HttpResponseRedirect(redirectUrl)
    if not request.POST:
        context = {
            'Status': 401  # change html file with inspect
        }
        return render(request, 'login/index.html', context)
    email = request.POST.get('Email')
    password = request.POST.get('Password')
    rememberMe = request.POST.get('RememberMe')
    listInput = [email, password]
    for i in listInput:
        if not i:
            context = {
                'Status': 403  # input incomplete
            }
            return render(request, 'login/index.html', context)
    customerInfo = Customer.objects.filter(Email=email, Password=password).first()
    courierInfo = Courier.objects.filter(Email=email, Password=password).first()
    bikeDeInfo = BikeDeliveryManger.objects.filter(Email=email, Password=password).first()
    if customerInfo:
        if customerInfo.isActive is False:
            context = {
                'Status': 404,  # account is inactive
            }
            return render(request, 'login/index.html', context)
        redirectUrl = reverse('portal-main')
        response = HttpResponseRedirect(redirectUrl)
        if rememberMe:
            set_cookie(response, 'Session', '{}'.format(customerInfo.Session))
        else:
            set_cookie(response, 'Session', '{}'.format(customerInfo.Session), 5)  # 5 hour
        return response
    elif courierInfo:
        if courierInfo.isActive is False:
            context = {
                'Status': 404,  # account is inactive
            }
            return render(request, 'login/index.html', context)
        redirectUrl = reverse('portal-main')
        response = HttpResponseRedirect(redirectUrl)
        if rememberMe:
            set_cookie(response, 'Session', '{}'.format(courierInfo.Session))
        else:
            set_cookie(response, 'Session', '{}'.format(courierInfo.Session), 5)  # 5 hour
        return response
    elif bikeDeInfo:
        if bikeDeInfo.isActive is False:
            context = {
                'Status': 404,  # account is inactive
            }
            return render(request, 'login/index.html', context)
        redirectUrl = reverse('portal-main')
        response = HttpResponseRedirect(redirectUrl)
        if rememberMe:
            set_cookie(response, 'Session', '{}'.format(bikeDeInfo.Session))
        else:
            set_cookie(response, 'Session', '{}'.format(bikeDeInfo.Session), 5)  # 5 hour
        return response
    else:
        context = {
            'Status': 402,  # email or password is wrong
        }
        return render(request, 'login/index.html', context)


def forgotPassword(request):
    return render(request, 'login/forgotPassword.html')
