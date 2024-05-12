from django.contrib import admin
from .models import Loans, Payments, PaymentsDetail, Customers

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['id','external_id','status','score']

@admin.register(Loans)
class LoansAdmin(admin.ModelAdmin):
    list_display = ['id','external_id']

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id','external_id']

@admin.register(PaymentsDetail)
class PaymentsDetailAdmin(admin.ModelAdmin):
    list_display = ['id']

