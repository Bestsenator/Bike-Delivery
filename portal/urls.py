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
    path('changeStBD/<int:code>', views.chStatusBikeDelivery, name='portal-chStatusBikeDelivery'),
    path('changeBDActive/', views.activeBikeDeliveryChange, name='portal-chBikeDeliveryActive'),
    path('requests/', views.requests, name='portal-requests'),
    path('accReqCourier/', views.acceptRequestCourier, name='portal-acceptRequestCourier'),
    path('rejReqCourier/<int:code>', views.rejectRequestCourier, name='portal-rejectRequestCourier'),
    path('profile/', views.profile, name='portal-profile'),
    path('changeInfo/', views.changeInfoProfile, name='portal-changeInfoProfile'),
    path('changePass/', views.changePassword, name='portal-changePassword'),


]
