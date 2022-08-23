from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

description =  """This is a basic e-commerce shop REST API.It implements some of the online shop operations, forexample
                 a user can create a cart, edit a cart ,remove and add items to a cart , can place and cancel an order,can register for an account.
                 It supports three types of user accouts;customer,traders and superusers accounts.
                 Access to different API endpoints resources depends user authenticity and permissions.



                 proudly : developed b [ Muwanguzi Joseph ]
                 muwaguzijoseph75@gmail.com

"""

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('debug_toolbar/',include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('api/',include("main.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("",include_docs_urls(title="JSHOP REST API",description=description)),

     ]

