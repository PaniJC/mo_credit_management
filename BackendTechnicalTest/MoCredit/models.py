from django.db import models

class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField()
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved = models.DateTimeField(auto_now_add=True)
    pass

class Loans(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField()
    contract_version = models.CharField(max_length=30, unique=True)
    maximum_payment_date = models.DateTimeField(auto_now_add=True)
    taken_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, to_field='id')
    outstanding_numeric = models.DecimalField(max_digits=12, decimal_places=2)
    pass

class Payments(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField()
    paid_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, to_field='id')
    pass

class PaymentsDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(Loans,on_delete=models.CASCADE, to_field='id')
    payment_id = models.ForeignKey(Payments,on_delete=models.CASCADE, to_field='id')
    pass





