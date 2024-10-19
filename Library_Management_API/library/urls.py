from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'checkouts', views.CheckoutViewSet)

urlpatterns = [
    path('books/', BookViewSet.as_view()),
]

urlpatterns += router.urls

#urlpatterns = router.urls