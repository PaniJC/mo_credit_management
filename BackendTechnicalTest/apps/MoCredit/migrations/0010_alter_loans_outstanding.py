# Generated by Django 5.0.6 on 2024-05-12 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoCredit', '0009_alter_loans_contract_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='outstanding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
