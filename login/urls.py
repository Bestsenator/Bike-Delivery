from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login-main'),
    path('check/', views.check, name='login-check'),
    path('forgotPassword/', views.forgotPassword, name='login-forgotPassword'),

]
