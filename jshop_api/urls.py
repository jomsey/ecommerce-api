from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls


urlpatterns = [

  path('debug_toolbar/',include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('api/',include("main.urls")),
    path("",include_docs_urls(title="JSHOP API",description="Cool online shop API")),
   
            
    
]
