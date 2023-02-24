from signup.models import Customer
import re


def checkSession(request):
    sesBrowser = request.COOKIES.get('Session')
    customerInfo = Customer.objects.filter(Session=sesBrowser).first()
    if customerInfo:
        if customerInfo.isActive is True:
            context = {
                'Status': 200,  # Customer
                'Info': customerInfo
            }
        else:
            context = {
                'Status': 201,  # Customer but inactive account
                'Info': customerInfo
            }
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
