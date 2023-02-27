from signup.models import Customer, Courier, BikeDeliveryManger
import re


def checkSession(request):
    sesBrowser = request.COOKIES.get('Session')
    customerInfo = Customer.objects.filter(Session=sesBrowser).first()
    info = None
    context = {}
    if customerInfo:
        info = customerInfo
        context = {
            'Character': 'Customer'
        }
    courierInfo = Courier.objects.filter(Session=sesBrowser).first()
    if courierInfo:
        info = courierInfo
        context = {
            'Character': 'Courier'
        }
    bikeDeInfo = BikeDeliveryManger.objects.filter(Session=sesBrowser).first()
    if bikeDeInfo:
        info = bikeDeInfo
        context = {
            'Character': 'BikeDeliveryManager'
        }
    if info is not None:
        if info.isActive is True:
            context['Status'] = 200  # valid
            context['Info'] = info
        else:
            context['Status'] = 201,  # valid but inactive account
            context['Info'] = info
    else:
        context = {
            'Status': 400  # not found session or member with this session
        }
    return context


def emailValidator(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False
