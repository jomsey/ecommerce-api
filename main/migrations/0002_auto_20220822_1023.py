# Generated by Django 3.2 on 2022-08-22 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_canceled',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending', max_length=10),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Complete', 'Complete')], default='Pending', max_length=10)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='main.order')),
            ],
        ),
    ]
