# Generated by Django 5.1.6 on 2025-04-28 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_alter_lease_payment_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentpayment',
            name='payment_method',
            field=models.CharField(choices=[('bank_transfer', 'Bank Transfer'), ('cash', 'Cash'), ('credit_card', 'Credit Card'), ('mobile_money', 'Mobile Money')], max_length=100),
        ),
    ]
