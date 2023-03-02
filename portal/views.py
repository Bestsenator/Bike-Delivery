import glob
import json
import os
import re

from django.core.files.storage import FileSystemStorage

from config import settings
from .models import Requests
import jdatetime
from django.core import serializers
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from funcs import auth
from funcs.cookies import set_cookie
from signup.models import BikeDelivery, \
    Courier, BikeDeliveryManger
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
            print('BIKE DELIVERY ==', bikeDeInfo)
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
            if request.COOKIES.get('Notif207') == '1':  # from changeBikeDeliveryActive --> changed
                context['ChangedBikeDeliveryActive'] = True
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


def chStatusBikeDelivery(request, code):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            bikeDeInfo = BikeDelivery.objects.filter(SuNumber=code).first()
            if bikeDeInfo:
                if bikeDeInfo.isActive is True:
                    bikeDeInfo.isActive = False
                else:
                    bikeDeInfo.isActive = True
                bikeDeInfo.save()
                redirectUrl = reverse('portal-bikeDelivery')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif204', '1', 0.0008)  # success change status Bike Delivery
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


def deleteBikeDelivery(request, code):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'BikeDeliveryActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            bikeDeInfo = BikeDelivery.objects.filter(SuNumber=code).first()
            if bikeDeInfo:
                bikeDeInfo.isDeleted = True  # for sign
                bikeDeInfo.isActive = False  # for inactive bike delivery
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


def activeBikeDeliveryChange(request):
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
                print(bikeDeInfo)
                print(bikeDeInfo.Name)
                print(bikeDeInfo.isActive)
                print(bikeDeInfo.isDeleted)
                bikeDeInfo.isActive = True
                bikeDeInfo.isDeleted = False
                bikeDeActiveInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber,
                                                               isDeleted=False).first()
                if bikeDeActiveInfo:
                    print('bikeDeActiveInfo.Name == ', bikeDeActiveInfo.Name)
                    print(bikeDeActiveInfo.isActive)
                    print(bikeDeActiveInfo.isDeleted)
                    bikeDeActiveInfo.isActive = False
                    bikeDeActiveInfo.isDeleted = True
                    bikeDeActiveInfo.DeleteTime = str(jdatetime.datetime.today())  # update Delete Time
                    bikeDeActiveInfo.save()
                bikeDeInfo.save()
                redirectUrl = reverse('portal-bikeDelivery')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif207', '1', 0.0008)  # success to change Bike Delivery Active
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


def requests(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Character'] = 'BikeDeliveryManager'
            bikeActiveInfo = BikeDelivery.objects.filter(BikeDeliveryManger=resAuth.get('Info').SuNumber
                                                         , isDeleted=False).first()
            if bikeActiveInfo:
                context['BDName'] = bikeActiveInfo.Name
                reqInfo = Requests.objects.filter(BikeDeliveryCode=bikeActiveInfo.SuNumber)
                if reqInfo:
                    listCourierCode = []
                    for item in reqInfo:
                        listCourierCode.append(item.CourierCode)
                    courierInfo = Courier.objects.filter(SuNumber__in=listCourierCode)
                    # Start -- Removing additional and security information from the information sent on the client side
                    for i in courierInfo:
                        i.Password = '0'
                        i.Session = '0'
                        i.isActive = '0'
                        i.BikeDeliveryCode = '0'
                    # End -- Removing
                    context['CourierInfo'] = courierInfo
                    courierInfo_json = json.dumps(serializers.serialize('json', courierInfo))
                    courierInfo_json = json.loads(courierInfo_json)
                    context['CourierInfo_json'] = courierInfo_json
                    context['ListRequest'] = reqInfo
                    reqInfo_json = json.dumps(serializers.serialize('json', reqInfo))
                    reqInfo_json = json.loads(reqInfo_json)
                    context['reqInfo_json'] = reqInfo_json
                else:
                    context['ListRequest'] = False
                if request.COOKIES.get('Notif207') == '1':
                    context['AcceptedRequestCourier'] = True  # from acceptRequestCourier --> accept
                if request.COOKIES.get('Notif208') == '1':
                    context['RejectedRequestCourier'] = True  # from rejectRequestCourier --> reject
                if checker.mobile(request) is True:  # for if with mobile origin menu hidden and hamburger manu visible
                    context['isMobile'] = True
                return render(request, 'portal/requests.html', context)
            else:
                context['Status'] = 401  # there is no Active sBike Delivery
                return render(request, 'portal/requests.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def acceptRequestCourier(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            if not request.GET:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/requests.html', context)
            code = request.GET.get('code')
            if not code:
                context['Status'] = 403  # input incomplete
                return render(request, 'portal/requests.html', context)
            reqInfo = Requests.objects.filter(Code=code).first()
            if reqInfo:
                courierInfo = Courier.objects.filter(SuNumber=reqInfo.CourierCode).first()
                courierInfo.BikeDeliveryCode = reqInfo.BikeDeliveryCode
                courierInfo.save()
                reqInfo.isChecked = True
                reqInfo.Status = True
                reqInfo.ActionTime = str(jdatetime.datetime.today())
                reqInfo.save()
                redirectUrl = reverse('portal-requests')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif207', '1', 0.0008)  # success to accept request from courier to bike delivery
                return response
            else:
                context['Status'] = 404  # request code is invalid
                return render(request, 'portal/requests.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def rejectRequestCourier(request, code):
    print(code)
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            reqInfo = Requests.objects.filter(Code=code).first()
            if reqInfo:
                reqInfo.isChecked = True
                reqInfo.Status = False
                reqInfo.ActionTime = str(jdatetime.datetime.today())
                reqInfo.save()
                redirectUrl = reverse('portal-requests')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif208', '1', 0.0008)  # success to reject request from Courier
                return response
            else:
                context['Status'] = 404  # code is wrong
                return render(request, 'portal/requests.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def profile(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'ProfileActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Character'] = 'BikeDeliveryManager'
            if request.COOKIES.get('Notif208') == '1':  # from changeInfo --> success
                context['SuccessChangeInfo'] = True
            if request.COOKIES.get('Notif209') == '1':  # from changePassword --> success
                context['SuccessChangePassword'] = True
            if checker.mobile(request) is True:  # for if with mobile origin menu hidden and hamburger manu visible
                context['isMobile'] = True
            context['Info'] = resAuth.get('Info')
            return render(request, 'portal/profile.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def changeInfoProfile(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Info'] = resAuth.get('Info')
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/profile.html', context)
            name = request.POST.get('Name')
            family = request.POST.get('Family')
            phone = request.POST.get('Phone')
            countryCode = request.POST.get('CountryCode')
            language = request.POST.get('Language')
            listInput = [name, family, phone, countryCode, language]
            for i in listInput:
                print(i)
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/profile.html', context)
            bikeInfo = BikeDeliveryManger.objects.filter(SuNumber=resAuth.get('Info').SuNumber).first()
            bikeInfo.Name = name
            bikeInfo.Family = family
            if not phone.isnumeric() or not countryCode.isnumeric():
                context = {
                    'Status': 408,  # phone or countryCode is invalid
                }
                return render(request, 'portal/profile.html', context)
            bikeInfo.CountryCode = countryCode
            if language == 'default':
                bikeInfo.Language = 'EN'
            elif language == 'EN' or language == 'FA':
                bikeInfo.Language = language
            else:
                context['Status'] = 402  # refresh Page
                return render(request, 'portal/profile.html', context)
            if len(phone) == 10:
                bikeInfo.Phone = phone
            else:
                context['Status'] = 402  # refresh Page
                return render(request, 'portal/profile.html', context)
            infoFile = request.FILES.get('Photo')
            if infoFile:
                sizeFile = infoFile.size / 1000  # in Kb
                if sizeFile > 500:
                    context['Status'] = 404  # size file more than 500KB
                    return render(request, 'portal/profile.html', context)
                if (infoFile.content_type == 'image/png') | (infoFile.content_type == 'image/jpg') | \
                   (infoFile.content_type == 'image/jpeg'):
                    print(infoFile.content_type)
                    typeFile = infoFile.content_type[6:]
                    folder = '{}img/profile-images/'.format(settings.STATIC_URL)
                    fullname = '{}.{}'.format(bikeInfo.SuNumber, typeFile)
                    files = glob.glob(
                        '{}img/profile-images/*'.format(settings.STATIC_URL))  # fetch all address files in pic_profiles
                    # -----START if profile is set then delete them-----
                    for file in files:
                        nameFile = file[26:]  # Separate the name from the full address
                        if nameFile == fullname:
                            location = os.path.join(settings.STATIC_URL, 'img/profile-images/')
                            path = os.path.join(location, nameFile)
                            os.remove(path)
                    # -----END if profile is set then delete them-----
                    fs = FileSystemStorage(location=folder)  # defaults to STATIC_URL
                    fs.save(name=fullname, content=infoFile)
                    bikeInfo.ImagePath = 'img/profile-images/{}'.format(fullname)
                else:
                    context['Status'] = 405  # file format is not supported
                    return render(request, 'portal/profile.html', context)
            bikeInfo.save()
            redirectUrl = reverse('portal-profile')
            response = HttpResponseRedirect(redirectUrl)
            set_cookie(response, 'Notif208', '1',
                       0.0008)  # success to changeInfo BikeDeliveryManager
            return response
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def changePassword(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Info'] = resAuth.get('Info')
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/profile.html', context)
            currentPassword = request.POST.get('CurrentPassword')
            newPassword = request.POST.get('NewPassword')
            retypeNewPassword = request.POST.get('RetypeNewPassword')
            listInput = [currentPassword, newPassword, retypeNewPassword]
            for i in listInput:
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/profile.html', context)
            if newPassword != retypeNewPassword:
                context['Status'] = 406  # newPassword and retypeNewPassword does not match
                return render(request, 'portal/profile.html', context)
            if resAuth.get('Info').Password != currentPassword:
                context['Status'] = 407  # currentPassword incorrect
                return render(request, 'portal/profile.html', context)
            if any(x.isupper() for x in newPassword) and any(x.islower() for x in newPassword):
                resBoth = True  # Upper and Lower is True
            else:
                resBoth = False  # Upper and Lower is False
            resNumber = bool(re.search(r'\d', newPassword))  # Number in String
            resSpecial = bool(any(c for c in newPassword if not c.isalnum() and not c.isspace()))  # SpecialChar in String
            if not resBoth or not resNumber or not resSpecial:
                context = {
                    'Status': 409,  # password format is invalid
                }
                return render(request, 'portal/profile.html', context)
            bikeInfo = BikeDeliveryManger.objects.filter(SuNumber=resAuth.get('Info').SuNumber).first()
            bikeInfo.Password = newPassword
            bikeInfo.save()
            redirectUrl = reverse('portal-profile')
            response = HttpResponseRedirect(redirectUrl)
            set_cookie(response, 'Notif209', '1',
                       0.0008)  # success to changePassword BikeDeliveryManager
            return response
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response


def deleteAcc(request):
    resAuth = auth.checkSession(request)
    if resAuth.get('Status') == 200:
        context = {
            'RequestsActive': 'active',
        }
        if resAuth.get('Character') == 'BikeDeliveryManager':
            context['Info'] = resAuth.get('Info')
            if not request.POST:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/profile.html', context)
            email = request.POST.get('Email')
            confirmAction = request.POST.get('ConfirmAction')
            listInput = [email, confirmAction]
            for i in listInput:
                if not i:
                    context['Status'] = 403  # input incomplete
                    return render(request, 'portal/profile.html', context)
            bikeInfo = BikeDeliveryManger.objects.filter(SuNumber=resAuth.get('Info').SuNumber).first()
            if bikeInfo.Email == email and confirmAction == 'on':
                bikeInfo.delete()
                redirectUrl = reverse('login-main')
                response = HttpResponseRedirect(redirectUrl)
                set_cookie(response, 'Notif210', '1',
                           0.0008)  # success to Delete Account
                return response
            else:
                context['Status'] = 402  # refresh page
                return render(request, 'portal/profile.html', context)
        else:
            redirectUrl = reverse('portal-main')
            return HttpResponseRedirect(redirectUrl)
    else:
        redirectUrl = reverse('login-main')
        response = HttpResponseRedirect(redirectUrl)
        set_cookie(response, 'Notif401', '1', 0.0008)  # session expired or not found session
        return response



