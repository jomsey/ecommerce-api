# Generated by Django 4.0 on 2022-08-09 19:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='product_name')),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(max_length=1000, verbose_name='product_description')),
                ('image_url', models.URLField(max_length=3000)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('product_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'ProductCategories',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ending_on', models.DateTimeField(auto_created=True)),
                ('starting_date', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=150)),
                ('products', models.ManyToManyField(to='main.Product')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField()),
                ('main_material', models.CharField(blank=True, max_length=200)),
                ('model', models.CharField(blank=True, max_length=200)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_made', models.DateField(auto_now_add=True)),
                ('review', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'very poor'), (2, 'poor'), (3, 'good'), (4, 'very good'), (4, 'excellent')], default='good', null=True, verbose_name='product_rating')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('product_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_count', models.PositiveIntegerField(default=1, verbose_name='number of product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='promotion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.promotion'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('date_made', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('D', 'Delivered')], default='P', max_length=1)),
                ('order_cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.cart')),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerWishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.productinstance')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='wish_list',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='main.customerwishlist'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.productinstance'),
        ),
    ]
