# Generated by Django 5.0.6 on 2024-05-09 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('status', models.SmallIntegerField()),
                ('score', models.DecimalField(decimal_places=2, max_digits=12)),
                ('preapproved', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.SmallIntegerField()),
                ('contract_version', models.CharField(max_length=30, unique=True)),
                ('maximum_payment_date', models.DateTimeField(auto_now_add=True)),
                ('taken_at', models.DateTimeField(auto_now_add=True)),
                ('outstanding_numeric', models.DecimalField(decimal_places=2, max_digits=12)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoCredit.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('total_amount', models.DecimalField(decimal_places=10, max_digits=20)),
                ('status', models.SmallIntegerField()),
                ('paid_at', models.DateTimeField(auto_now_add=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoCredit.customers')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentsDetail',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=10, max_digits=20)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoCredit.loans')),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MoCredit.payments')),
            ],
        ),
    ]