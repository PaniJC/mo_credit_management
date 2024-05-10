from django.contrib import admin
from .models import Loans, Payments, PaymentsDetail, Customers

admin.site.register(Loans)
admin.site.register(Payments)
admin.site.register(PaymentsDetail)
admin.site.register(Customers)

