from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:product_id>/', views.PurchaseCreate.as_view(), name='buy'),
    path('buy_all/', views.PurchaseCreateAll.as_view(), name='buy_all'),
    path('purchase_success/', views.PurchaseSuccess.as_view(), name='purchase_success'),
    path('cart/', views.cart, name='cart'),
    path('edit_cart/', views.edit_cart, name='edit_cart'),
]
