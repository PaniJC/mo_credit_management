from django.urls import path
from apps.MoCredit.api.api import customer_api_view,loans_api_view, by_external_id, balance, create_customer,loans_by_customer, create_loan

urlpatterns = [
    path('customers/',customer_api_view, name='customers_api'),
    path('loans/',loans_api_view, name='loans_api'),
    path('customers/by_external_id/<str:external_id>',by_external_id, name='customers_api'),
    path('customers/balance/<str:external_id>',balance, name='customers_api'),
    path('customers/create_customer/',create_customer, name='customers_api'),
    path('loans/loans_by_customer/<str:customer_external_id>',loans_by_customer, name='loans_api'),
    path('loans/create_loan/',create_loan, name='loans_api'),



]
