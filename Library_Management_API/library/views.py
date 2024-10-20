from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, permissions
from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions,IsAdminUser
from rest_framework.generics import ListAPIView
from .models import Book, Database
from rest_framework.decorators import permission_classes,authentication_classes
from .serializers import BookSerializer,DatabaseSerializer

from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from .filters import BookFilter
from django.urls import reverse

"""
creating a read only permission to make sure that only admins can make the relevant changes
"""
class BookPermission(permissions.BasePermission):
    #This has permission is good with creating of a new object
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.has_perm('Library.create')
        return True
    #recommended when making changes to existing objects. \
        
    def has_object_permission(self, request, view, obj):
        if view.action in ['update','partial_update']:
            return request.user.has_perm('Library.edit')
        elif view.action == 'destroy':
            return request.user.has_perm('Library.delete')
        return True

"""
creating views for the database.
Only the superuser can create CUD(CREATE, UPDATE or DELETE) the database and content
admins can perform CRUD operations on the book data
"""
class ObjectReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser #we want only superusers to have the rest of the permissions for crud operations
    
#Next, we create the databaseviewset
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class DatabaseView(viewsets.ModelViewSet):
    """
    {
        "database_name":"samplename"
    }
    This is a post method that expects this input. Only superusers have access
    """
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    permission_classes=[ObjectReadOnlyPermission]
#Creating the view for books

@permission_classes([IsAuthenticated,BookPermission])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class BookView(viewsets.ModelViewSet):
    """
    post method. Only admins can add, edit, or delete books
    It also allows get for non admins
    You can filter by title,isbn,published_date and number_of_copies and number_of_copies__gt=int
    """

    filter_backends = [DjangoFilterBackend] # Filtering the backend code differently
    filterset_class = BookFilter # Filtering the books  
    serializer_class = BookSerializer #Book Serializer
    queryset = Book.objects.all().order_by('-published_date')
    


class BookList(ListAPIView):
    """
    The get method is used here to
    List the number of books present with the corresponding details
    """

    filter_backends = [DjangoFilterBackend] # Filtering the backend code differently
    filterset_class = BookFilter # Filtering the books    
    serializer_class = BookSerializer # Setting the serializer route
    queryset = Book.objects.all().order_by('-published_date')
