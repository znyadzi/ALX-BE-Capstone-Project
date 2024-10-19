from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from library import views
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'checkouts', views.CheckoutViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url='', permanent=False)), # Redirect to /api/books/
    path('api/', include(router.urls)),
]