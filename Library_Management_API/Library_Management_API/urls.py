"""
URL configuration for Library_Management_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
# This is a view that takes in the title, default api version and description
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="1.0.0",
        description="API documentation for the app",
    ),
    public=True,
)

urlpatterns = [
    path('secret-admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('subscribe/',include('notifications.urls')),
    path('api/',include('Library.urls')),
    path('api/',include('transactions.urls')),
    path('',schema_view.with_ui('swagger',cache_timeout=0),name="swagger-schema"), 
   
]
