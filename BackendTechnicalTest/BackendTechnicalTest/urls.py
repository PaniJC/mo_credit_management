"""
URL configuration for BackendTechnicalTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.MoCredit.services.customers_services import create_customer, get_customer_by_external_id,get_customer_balance
from apps.MoCredit.services.loan_services import create_loan, get_loans_by_customer
from apps.MoCredit.services.payments_services import create_payment, get_payments_by_customer

schema_view = get_schema_view(
   openapi.Info(
      title="MoCredit Documentation",
      default_version='v1',
      description="Test Backend MoCredit",
      terms_of_service="https://www.mocredit_test.com/",
      contact=openapi.Contact(email="juan77camilo@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/create', create_customer, name='create_customer'),
    path('customers/get_by_external_id', get_customer_by_external_id, name='get_customer_by_external_id'),
    path('customers/get_customer_balance', get_customer_balance, name='get_customer_balance'),
    path('loans/create', create_loan, name='create_loan'),
    path('loans/get_by_customer', get_loans_by_customer, name='get_loans_by_customer'),
    path('payments/create', create_payment, name='create_payment'),
    path('payments/get_payments_by_customer', get_payments_by_customer, name='get_payments_by_customer'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')

]
