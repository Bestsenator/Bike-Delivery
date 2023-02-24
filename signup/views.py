import jdatetime
from datetime import timezone
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs.cookies import set_cookie
from .models import Customer, VerifyCode
from funcs import auth
import re
from secrets import token_urlsafe


# Create your views here.


timeExpireCode = 300  # 5 minute


def index(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        redirectUrl = reverse('portal-main')
        return HttpResponseRedirect(redirectUrl)
    return render(request, 'signup/index.html')


def check(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        redirectUrl = reverse('portal-main')
        return HttpResponseRedirect(redirectUrl)
    if not request.POST:
        context = {
            'Status': 401  # refresh page
        }
        return render(request, 'signup/index.html', context)
    name = request.POST.get('Name')
    family = request.POST.get('Family')
    countryCode = request.POST.get('CountryCode')
    phone = request.POST.get('Phone')
    email = request.POST.get('Email')
    password = request.POST.get('Password')
    retypePassword = request.POST.get('RetypePassword')
    terms = request.POST.get('Terms')
    listInput = [name, family, countryCode, phone,
                 email, password, retypePassword, terms]
    for i in listInput:
        print(i)
        if not i:
            context = {
                'Status': 402  # refresh page
            }
            return render(request, 'signup/index.html', context)
    if not phone.isnumeric() or not countryCode.isnumeric():
        context = {
            'Status': 407,  # phone or countryCode is invalid
        }
        return render(request, 'signup/index.html', context)
    memberInfo = Customer.objects.filter(Email=email).first()
    if memberInfo:
        context = {
            'Status': 406,  # email exist
        }
        return render(request, 'signup/index.html', context)
    resAuthEmail = auth.emailValidator(email)
    if resAuthEmail is False:
        context = {
            'Status': 403,  # input format is invalid
        }
        return render(request, 'signup/index.html', context)
    if len(phone) != 10:
        context = {
            'Status': 403,  # input format is invalid
        }
        return render(request, 'signup/index.html', context)
    if password != retypePassword:
        context = {
            'Status': 404,  # password and retypePassword does not match
        }
        return render(request, 'signup/index.html', context)
    if any(x.isupper() for x in password) and any(x.islower() for x in password):
        resBoth = True  # Upper and Lower is True
    else:
        resBoth = False  # Upper and Lower is False
    resNumber = bool(re.search(r'\d', password))  # Number in String
    resSpecial = bool(any(c for c in password if not c.isalnum() and not c.isspace()))  # SpecialChar in String
    if not resBoth or not resNumber or not resSpecial:
        context = {
            'Status': 405,  # password format is invalid
        }
        return render(request, 'signup/index.html', context)
    if terms != 'on':
        context = {
            'Status': 403,  # input format is invalid
        }
        return render(request, 'signup/index.html', context)
    sesID = token_urlsafe(100)
    Customer.objects.create(Name=name, Family=family, Email=email,
                            Phone=phone, Password=password, Session=sesID, CountryCode=countryCode)
    VerifyCode.objects.create(Email=email, Session=sesID)
    redirectUrl = reverse('signup-verify')
    response = HttpResponseRedirect(redirectUrl)
    set_cookie(response, 'Session', '{}'.format(sesID))
    return response


def verify(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 400:
        redirectUrl = reverse('login-main')
        return HttpResponseRedirect(redirectUrl)
    elif resAuth.get('Status') == 200:
        redirectUrl = reverse('portal-main')
        return HttpResponseRedirect(redirectUrl)
    customerInfo = Customer.objects.filter(Session=request.COOKIES.get('Session')).first()
    context = {
        'Email': customerInfo.Email,
        'SuNumber': customerInfo.SuNumber,
    }
    if request.COOKIES.get('Notif202') == '1':
        context['SendCodeSuccess'] = True
    if request.COOKIES.get('Notif401') == '1':
        context['CodeNotExpire'] = True
    if request.COOKIES.get('Notif402') == '1':
        context['RefreshPage'] = True
    return render(request, 'signup/verify.html', context)


def verifyCheck(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 400:
        redirectUrl = reverse('login-main')
        return HttpResponseRedirect(redirectUrl)
    elif resAuth.get('Status') == 200:
        redirectUrl = reverse('portal-main')
        return HttpResponseRedirect(redirectUrl)
    if not request.POST:
        context = {
            'Status': 401,  # input error
        }
        return render(request, 'signup/verify.html', context)
    code = request.POST.get('Code')
    suNumber = request.POST.get('SuNumber')
    listInput = [suNumber, code]
    for i in listInput:
        if not i:
            context = {
                'Status': 403,  # input incomplete
            }
            return render(request, 'login/index.html', context)
    verifyInfo = VerifyCode.objects.filter(Email=resAuth.get('Info').Email).first()
    if verifyInfo:
        context = {
            'Email': resAuth.get('Info').Email,
            'SuNumber': resAuth.get('Info').SuNumber,
        }
        timeNow = jdatetime.datetime.now().replace(tzinfo=None)
        timeNow = jdatetime.datetime.strptime(str(timeNow), '%Y-%m-%d %H:%M:%S.%f')
        timeSend = verifyInfo.Time.replace(tzinfo=None)
        timeSend = jdatetime.datetime.strptime(str(timeSend), '%Y-%m-%d %H:%M:%S.%f')
        print((timeNow - timeSend).total_seconds())
        if (timeNow - timeSend).total_seconds() > timeExpireCode:  # time expire any code is 5 minute
            context['Status'] = 404  # code has expired
            return render(request, 'signup/verify.html', context)
        if verifyInfo.Code != int(code):
            context['Status'] = 405  # code incorrect
            return render(request, 'signup/verify.html', context)
        resAuth.get('Info').isActive = True
        resAuth.get('Info').save()
        verifyInfo.delete()
        redirectUrl = reverse('portal-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif200', '1', 0.0008)
        return response
    else:
        redirectUrl = reverse('signup-verify')
        return HttpResponseRedirect(redirectUrl)







