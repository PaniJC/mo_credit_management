# Generated by Django 5.0.6 on 2024-05-10 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoCredit', '0002_rename_preapproved_customers_preapproved_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='loans',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='paymentsdetail',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]