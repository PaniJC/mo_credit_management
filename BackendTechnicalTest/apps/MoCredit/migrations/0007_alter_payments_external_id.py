# Generated by Django 5.0.6 on 2024-05-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoCredit', '0006_alter_payments_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='external_id',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]