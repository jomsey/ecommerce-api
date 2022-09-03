from django.contrib import admin
from . models import *


admin.site.register(Customer)
admin.site.register(ProductReview)
admin.site.register(Order)
admin.site.register(CustomerWishList)
admin.site.register(Trader)
admin.site.register(Promotion)
admin.site.register(Payment)
admin.site.register(Subcategory)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['cart_uuid','date_created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display=['name','price','category','trader','promotion','date_added']


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
	pass