# Generated by Django 4.0.6 on 2022-11-20 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cart_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_created',
            field=models.DateField(auto_created=True),
        ),
        migrations.CreateModel(
            name='ProductsCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('products', models.ManyToManyField(to='store.product')),
            ],
        ),
    ]