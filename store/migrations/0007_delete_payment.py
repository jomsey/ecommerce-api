# Generated by Django 3.2 on 2022-12-15 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_payment_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
