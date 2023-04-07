from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('inbound/create/', views.inbound_create, name='inbound_create'),
    path('outbound/<int:product_id>/create/', views.outbound_create, name='outbound_create'),
    path('inventory/', views.inventory, name='inventory'),
]