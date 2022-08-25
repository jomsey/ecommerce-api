# Generated by Django 4.0.6 on 2022-08-25 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_image_url_alter_product_product_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='product sub category', max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateField(auto_now_add=True, verbose_name='date added to store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='product description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='This is the name of the product', max_length=200, verbose_name='product name'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subcategory'),
        ),
    ]
