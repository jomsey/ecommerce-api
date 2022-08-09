from cgitb import lookup
from rest_framework_nested import routers
from . import views
from django.urls import path,include


router = routers.SimpleRouter()

#parent routers
router.register(viewset = views.ProductViewSet,prefix = 'products',basename='products')
router.register(viewset=views.ProductCategoryViewSet,prefix='categories')
router.register(viewset=views.PromotionViewSet,prefix='promotions')

#product routers
product_routers = routers.NestedSimpleRouter(router,'products',lookup='product')
product_routers.register('reviews',views.ProductReviewViewSet,basename='reviews')
product_routers.register('specifications',views.ProductSpecificationViewSet)

#product categories routers
category_routers = routers.NestedSimpleRouter(router,'categories',lookup='category')
category_routers.register('products',views.ProductViewSet,basename='products')

#promotions routers 
promotion_routers = routers.NestedSimpleRouter(router,'promotions',lookup='promotion')
promotion_routers.register('products',views.ProductViewSet,basename='products')



urlpatterns=[ 
             path('',include(router.urls)),
             path('',include(product_routers.urls)),
             path('',include(category_routers.urls)),
             path('',include(promotion_routers.urls)),
             
             ]

