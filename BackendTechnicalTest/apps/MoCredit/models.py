from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Customers(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(validators=[
            MinValueValidator(1, message="The min allowed value is 1"),
            MaxValueValidator(2, message="Te max allowed value is 2")
        ])
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(auto_now_add=True)
    pass


class Loans(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(default=2, validators=[
            MinValueValidator(1, message="The min allowed value is 1"),
            MaxValueValidator(4, message="Te max allowed value is 4")
        ])
    contract_version = models.CharField(max_length=30,blank=True, null=True)
    maximum_payment_date = models.DateTimeField(auto_now_add=True)
    taken_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, to_field='id')
    outstanding = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    pass

class Payments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField(validators=[
            MinValueValidator(1, message="The min allowed value is 1"),
            MaxValueValidator(2, message="Te max allowed value is 2")
        ])
    paid_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, to_field='id')
    pass

class PaymentsDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(Loans,on_delete=models.CASCADE, to_field='id')
    payment_id = models.ForeignKey(Payments,on_delete=models.CASCADE, to_field='id')
    pass




