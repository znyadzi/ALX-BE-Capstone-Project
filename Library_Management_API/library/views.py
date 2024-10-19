from django.shortcuts import render
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
        try:
            book = self.get_object()  # Get the book instance using the primary key (pk)

            if book.is_checked_out:
                return Response({"detail": "Book is already checked out."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user  # Get the currently authenticated user

            # Create a new checkout entry
            checkout = Checkout.objects.create(
                user=user,
                book=book,
                checkout_date=datetime.now(),
                due_date=datetime.now() + timedelta(days=14)  # 14-day due date
            )

            book.is_checked_out = True
            book.save()

            serializer = CheckoutSerializer(checkout)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Checkout failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        try:
            checkout = self.get_object() # Get the checkout instance using the primary key (pk)

            if checkout.return_date is not None:
                return Response({"detail": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

            checkout.return_date = datetime.now()
            checkout.save()

            book = checkout.book
            book.is_checked_out = False
            book.save()

            serializer = CheckoutSerializer(checkout)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Checkout.DoesNotExist:
            return Response({"detail": "Checkout not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Return failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
