from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='portal-main'),
    #  Path for Bike Delivery Manager
    path('bikeDelivery/', views.bikeDelivery, name='portal-bikeDelivery'),
    path('addBikeDelivery/', views.addBikeDelivery, name='portal-addBikeDelivery'),
    path('changeInfoBD/', views.changeInfoBikeDelivery, name='portal-changeInfoBikeDelivery'),
    path('deleteBD/<int:code>', views.deleteBikeDelivery, name='portal-deleteBikeDelivery'),
    path('coDeleteBD/', views.coDeleteBikeDelivery, name='portal-coDeleteBikeDelivery'),


]
