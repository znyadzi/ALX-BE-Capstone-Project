from django.shortcuts import render,get_object_or_404
from .models import Book, Database
from rest_framework import viewsets, permissions
from .serializers import BookSerializer,DatabaseSerializer
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions,IsAdminUser
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from .filters import BookFilter
from django.urls import reverse

"""Create your views here.

we create a custom readonly permission
I INTEND TO ENSURE THAT ONLY THOSE WITH ADMIN PRIVILEGES CAN MAKE THESE CHANGES"""
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

"""we create the viewset for database creation.
where only the superuser can create those databases or delete them,
the admin can only perform crud operations on books"""
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
#Next, we create the Bookviewset
@permission_classes([IsAuthenticated,BookPermission])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class BookView(viewsets.ModelViewSet):
    """
    post method. Only admins can add, edit, or delete books
    It also allows get for non admins
    You can filter by title,isbn,published_date and number_of_copies and number_of_copies__gt=int
    """
    queryset = Book.objects.all().order_by('-published_date')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend] #It is a good filter approach that allows the use of different filter approaches
    filterset_class = BookFilter #I pass the bookfilter so that I can now search with greater than

class BookList(ListAPIView):
    """
    This is a get method
    It lists the number of books present and their details
    """
    
    serializer_class = BookSerializer #I have to serialize the results
    queryset = Book.objects.all().order_by('-published_date')
    filter_backends = [DjangoFilterBackend] #It is a good filter approach that allows the use of different filter approaches
    filterset_class = BookFilter #I pass the bookfilter so that I can now search with greater than