from django.contrib import admin
from . models import *


admin.site.register(ProductReview)
admin.site.register(Order)
admin.site.register(CustomerWishList)
admin.site.register(Trader)
admin.site.register(Promotion)
admin.site.register(Subcategory)

admin.site.site_header = "JSHOP API ADMIN PANEL"
admin.site.index_title = "Admin"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductsCollection)
class ProductsCollectionAdmin(admin.ModelAdmin):
	list_display=["title"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['cart_uuid','date_created']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display=['name','price','category','trader','promotion','date_added']
	list_editable=["price","promotion",]
	list_per_page = 20
	list_filter = ["category"]
	search_fields=["name"]



@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
	list_display = ["product","product_count","product_uuid"]
	list_per_page = 20

@admin.register(WishListProductInstance)
class WishListProductInstanceAdmin(admin.ModelAdmin):
	list_display = ["product","product_uuid"]
	list_per_page = 20

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
	pass