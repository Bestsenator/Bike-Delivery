from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='signup-main'),
    path('check/', views.check, name='signup-check'),
    path('verify/', views.verify, name='signup-verify'),
    path('verifyCheck/', views.verifyCheck, name='signup-verifyCheck'),
    # path('resendCode/', views.resendCode, name='signup-resendCode'),
]
