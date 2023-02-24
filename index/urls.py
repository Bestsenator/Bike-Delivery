from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-main'),
    path('logout/', views.logout, name='logout'),
]
