from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from .models import Book, User, Checkout
from .serializers import BookSerializer, UserSerializer, CheckoutSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated]) #Added permission class here
    def checkout(self, request, pk=None):
        # ... (checkout logic remains the same)

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser] # Admins only can manage users
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CheckoutViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] # Only authenticated users can view checkouts
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated]) #Added permission class here
    def return_book(self, request, pk=None):
        # ... (return logic remains the same)