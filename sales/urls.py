# sales/urls.py
from django.urls import path
from . import views

app_name = 'sales'  # This enables {% url 'sales:bill_list' %} and so on

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),

    path('bills/', views.bill_list, name='bill_list'),
    path('bills/create/', views.bill_create, name='bill_create'),
    path('bills/<int:pk>/', views.bill_detail, name='bill_detail'),
    path('bills/<int:pk>/pdf/', views.generate_bill_pdf, name='bill_pdf'),
]
