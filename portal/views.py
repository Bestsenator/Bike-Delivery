import json

import jdatetime
from django.core import serializers
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs import auth
from funcs.cookies import set_cookie
from signup.models import BikeDelivery
from funcs import checker
# Create your views here.


def index(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'DashboardActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            bikeDeInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber).first()  # fetch info bikeDelivery for Manager
            if not bikeDeInfo:
                context['Status'] = 401  # Bike Delivery is not registered
            context['Character'] = 'BikeDeliveryManager'
        if checker.mobile(request) is True:
            context['isMobile'] = True
        return render(request, 'portal/index.html', context)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def bikeDelivery(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Character'] = 'BikeDeliveryManager'
            bikeDeInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber, isDeleted=False).first()  # fetch info bikeDelivery for Manager
            if bikeDeInfo:
                context['Info'] = bikeDeInfo
            else:
                context['Status'] = 401  # Bike Delivery is not registered
                context['Info'] = False
            deBikeInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber, isDeleted=True)
            if deBikeInfo:
                deBikeInfo_json = json.dumps(serializers.serialize('json', deBikeInfo))
                deBikeInfo_json = json.loads(deBikeInfo_json)
                context['ListDeletedBD'] = deBikeInfo
                context['ListDeletedBD_json'] = deBikeInfo_json
            else:
                context['ListDeletedBD'] = False
            if request.COOKIES.get('Notif202') == '1':  # from addBikeDelivery --> success
                context['SuccessSaveBikeDelivery'] = True
            if request.COOKIES.get('Notif203') == '1':  # from changeInfoBikeDelivery --> changed
                context['ChangedInfoBD'] = True
            if request.COOKIES.get('Notif204') == '1':  # from chStatusBikeDelivery --> changed
                context['ChangedStatusBD'] = True
            if request.COOKIES.get('Notif205') == '1':  # from DeleteBikeDelivery --> success
                context['DeletedBD'] = True
            if request.COOKIES.get('Notif206') == '1':  # from coDeleteBikeDelivery --> deleted
                context['CompleteDeletedBD'] = True
            if checker.mobile(request) is True:  # for if with mobile origin menu hidden and hamburger manu show
                context['isMobile'] = True
            return render(request, 'portal/bikeDelivery.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def addBikeDelivery(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/bikeDelivery.html', context)
            name = request.POST.get('Name')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone')
            countryCode = request.POST.get('CountryCode')
            listInput = [name, address, phone, countryCode]
            for i in listInput:
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/bikeDelivery.html', context)
            BikeDelivery.objects.create(Name=name, Address=address, Phone=phone,
                                        CountryCode=countryCode, BikeDeliveryManger=resAuth.get('Info').SuNumber)
            redirectUrl = reverse('portal-bikeDelivery')
            response = HttpResponseRedirect(redirectUrl)
            set_cookie(response, 'Notif202', '1', 0.0008)  # success to save Bike Delivery
            return response
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def changeInfoBikeDelivery(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/bikeDelivery.html', context)
            name = request.POST.get('Name')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone')
            countryCode = request.POST.get('CountryCode')
            listInput = [name, address, phone, countryCode]
            for i in listInput:
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/bikeDelivery.html', context)
            bikeDeInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber).first()
            bikeDeInfo.Name = name
            bikeDeInfo.Address = address
            bikeDeInfo.Phone = phone
            bikeDeInfo.CountryCode = countryCode
            bikeDeInfo.save()
            redirectUrl = reverse('portal-bikeDelivery')
            response = HttpResponseRedirect(redirectUrl)
            set_cookie(response, 'Notif203', '1', 0.0008)  # success change Bike Delivery Info
            return response
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def chStatusBikeDelivery(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/bikeDelivery.html', context)
            name = request.POST.get('Name')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone')
            countryCode = request.POST.get('CountryCode')
            listInput = [name, address, phone, countryCode]
            for i in listInput:
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/bikeDelivery.html', context)
            bikeDeInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber).first()
            bikeDeInfo.isActive = False
            bikeDeInfo.save()
            redirectUrl = reverse('portal-bikeDelivery')
            response = HttpResponseRedirect(redirectUrl)
            set_cookie(response, 'Notif204', '1', 0.0008)  # success change status Bike Delivery
            return response
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def deleteBikeDelivery(request, code):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            bikeDeInfo = BikeDelivery.objects.filter(SuNumber=code).first()
            if bikeDeInfo:
                bikeDeInfo.isDeleted = True
                bikeDeInfo.DeleteTime = str(jdatetime.datetime.today())
                bikeDeInfo.save()
                redirectUrl = reverse('portal-bikeDelivery')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif205', '1', 0.0008)  # deleted Bike Delivery
                return response
            else:
                context['Status'] = 404  # code is wrong
                return render(request, 'portal/bikeDelivery.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def coDeleteBikeDelivery(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            if not request.GET:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/bikeDelivery.html', context)
            code = request.GET.get('code')
            if not code:
                context['Status'] = 403  # input incomplete
                return render(request, 'portal/bikeDelivery.html', context)
            bikeDeInfo = BikeDelivery.objects.filter(SuNumber=code).first()
            if bikeDeInfo:
                bikeDeInfo.delete()
                redirectUrl = reverse('portal-bikeDelivery')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif206', '1', 0.0008)  # complete deleted Bike Delivery
                return response
            else:
                context['Status'] = 404  # bike delivery code is invalid
                return render(request, 'portal/bikeDelivery.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response
