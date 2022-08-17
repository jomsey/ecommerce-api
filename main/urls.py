from cgitb import lookup
from rest_framework_nested import routers
from . import views
from django.urls import path,include


router = routers.SimpleRouter()

#parent routers
router.register(viewset=views.CustomerViewSet,prefix='customer',basename='customer')
router.register(viewset = views.ProductViewSet,prefix = 'products',basename='products')
router.register(viewset=views.FeaturedProductViewSet,prefix='featured_products')
router.register(viewset=views.ProductCategoryViewSet,prefix='categories')
router.register(viewset=views.PromotionViewSet,prefix='promotions')
router.register(viewset=views.CartViewSet,prefix='cart',basename='cart')
router.register(viewset=views.CustomerWishListViewSet,prefix='wish_list',basename='wish_list')

#product routers
product_routers = routers.NestedSimpleRouter(router,'products',lookup='product')
product_routers.register('reviews',views.ProductReviewViewSet,basename='reviews')
product_routers.register('specifications',views.ProductSpecificationViewSet)

#product categories routers
category_routers = routers.NestedSimpleRouter(router,'categories',lookup='category')
category_routers.register('products',views.ProductViewSet,basename='products')

#promotions routers 
promotion_routers = routers.NestedSimpleRouter(router,'promotions',lookup='promotion')
promotion_routers.register('promotion_products',views.ProductViewSet,basename='products')

#cart routers
cart_routers = routers.NestedSimpleRouter(router,'cart',lookup='cart')
cart_routers.register('cart_products',views.ProductInstanceViewSet,basename='products_instances')

#customer routers
customer_routers  = routers.NestedSimpleRouter(router,'customer',lookup='customer')
customer_routers.register('orders',views.OrderViewSet,basename='customer_orders')

#wish list routers
wish_list_routers = routers.NestedSimpleRouter(router,'wish_list',lookup='wish_list')
wish_list_routers.register('wish_list_products',views.ProductInstanceViewSet,basename='products_instances')



urlpatterns=[ 
             path('',include(router.urls)),
             path('',include(product_routers.urls)),
             path('',include(category_routers.urls)),
             path('',include(promotion_routers.urls)),
             path('',include(cart_routers.urls)),
             path('',include(customer_routers.urls)),
             path('',include(wish_list_routers.urls))
             
             ]

