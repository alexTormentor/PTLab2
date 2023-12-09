from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/', views.PurchaseCreate.as_view(), name='buy'),
    path('cart/', views.cart, name='cart'),
    path('edit_cart/', views.edit_cart, name='edit_cart'),
]
