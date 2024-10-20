from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from rest_framework import response,status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Database,Book
User = get_user_model()
# Create your tests here.

class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        admin_group = Group.objects.create(name='Admin') 
        student_group = Group.objects.create(name='Student') 
        self.database_url = reverse('database-list') 
        self.books_url = reverse('books-list')
        self.signup_url = reverse('signup') 
        self.login_url = reverse('login') 
        
        book_type = ContentType.objects.get(app_label='Library',model='book')
       
        create_data_permission,_ = Permission.objects.get_or_create(
            codename='create',
            name='can add a new book',
            content_type=book_type
        )
        edit_data_permission,_ = Permission.objects.get_or_create(
            codename='edit',
            name='can update an existing book',
            content_type=book_type
        )
        delete_data_permission,_ = Permission.objects.get_or_create(
            codename='delete',
            name='can delete an existing book',
            content_type=book_type
        )
        #we then add these permissions to the admin group
        admin_group.permissions.add(edit_data_permission,delete_data_permission,create_data_permission)
        #we create a normal user, student, admin, and the  a superuser
        self.newstudent_user = self.client.post(self.signup_url,{
            "username":"Rasha",
            "email":"rasha@gmail.com",
            "password":"rasha1t123",
            "first_name":"Rashan",
            "last_name":"Williams",
            "date_of_birth":"2000-10-01",
            "profile_image":"",
            "role": "student",
            "active_status":True
        })
        self.newadmin_user = self.client.post(self.signup_url,{
            "username":"Yasmin",
            "email":"yasmin@gmail.com",
            "password":"yAsming34t",
            "first_name":"Yasmin",
            "last_name":"Modani",
            "date_of_birth":"2000-10-12",
            "profile_image":"",
            "role": "admin",
            "active_status":True
        })
        self.superuser = User.objects.create_superuser(
            username='Sharon45',
            email='sharon45@gmail.com',
            password='sHazine3y56',
            first_name = 'Sharon',
            last_name = 'Jenkins'
            
        )
        #creating a test database to check read functionality
        self.client.login(email='sharon45@gmail.com',password=('sHazine3y56'))
        self.client.post(self.database_url,{
            'database_name':'Literature'
        })
        self.client.post(self.database_url,{
            'database_name':'History'
        })
        database = Database.objects.get(database_name='History')
        database_id = database.id
        self.client.post(self.books_url,{
            "title":"Mythical Philosophy",
            "author":"Jackie,Newman",
            "isbn":"8741762779715",
            "published_date":"2010-11-01",
            "number_of_copies":3,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.client.logout()
    def test_database_by_student_creation(self):
        #first, we test whether a regular user can create a database
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rashalt123."
        })
        token = response.data.get('token')
        print(f'Token to Rashan testing database student creation {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(self.database_url,{
            'database_name':'Physics'
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after student creates database trial {response.data}')
    def test_database_by_admin_creation(self):
        #first, we test whether a regular user can create a database
        response = self.client.post(self.login_url,{
            "email":"yasmin@gmail.com",
            "password":"yAsming34t."
        })
        token = response.data.get('token')
        print(f'Token to Yasmin testing database admin creation {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(self.database_url,{
            'database_name':'Biology'
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after admin creates database trial {response.data}')
    def test_database_by_superuser_creation(self):
        # we test if a regular user can create a database
        response = self.client.post(self.login_url,{
            "email":"sharon45@gmail.com",
            "password":"sHazine3y56."
        })
        token = response.data.get('token')
        print(f'Token to Sharon45 testing database superuser creation {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(self.database_url,{
            'database_name':'English'
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        print(f'Response data check after superuser creates database trial {response.data}')
    def test_database_read_by_admin(self):
        # we test whether a regular user can read existing databases
        response = self.client.post(self.login_url,{
            "email":"yasmin@gmail.com",
            "password":"yAsming34t" # allows us to log in and access the token
        })
        token = response.data.get('token')
        print(f'Token to Yasmin testing database admin Read {token}') 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #token is passed under credentials
        response = self.client.get(self.database_url)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(f'Response data check if admin can see available database {response.data}')
    def test_database_read_by_studeht(self):
        #first, we test whether a regular user can see the database present
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token')
        print(f'Token to Rashan testing database student Read {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #details are passed using credentials
        response = self.client.get(self.database_url)
        self.assertEquals(response.status_code,status.HTTP_200_OK) #allows us to check whether the status code is the same
        print(f'Response data check if student can see available database {response.data}') #print function is used as a test to see what data is printed out
    def test_database_update_for_admin(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"yasmin@gmail.com",
            "password":"yAsmig34t"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Yasmin testing database admin update {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.put(self.database_detail_url,{
            'database_name':'LibraryMan'
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after admin updates database trial {response.data}')
    def test_database_update_for_student(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Rashan testing database student update {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.put(self.database_detail_url,{
            'database_name':'LibraryMan'
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after student updates database trial {response.data}')
    def test_database_update_for_superuser(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"sharon45@gmail.com",
            "password":"sHazine3y56"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Sharon testing database superuser update {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.put(self.database_detail_url,{
            'database_name':'LibraryMan'
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(f'Response data check after superuser updates database trial {response.data}')
    def test_database_delete_for_admin(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"yasmin@gmail.com",
            "password":"yAsming34t"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Yasmin testing database admin delete {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.delete(self.database_detail_url)
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after admin deletes database trial {response.data}')
    def test_database_delete_for_student(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Rashan testing database student delete {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.delete(self.database_detail_url)
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after student deletes database trial {response.data}')
    def test_database_delete_for_superuser(self):
        #first, we test whether a regular user can update
        response = self.client.post(self.login_url,{ #WE LOGIN USER
            "email":"sharon45@gmail.com",
            "password":"sHazine3y56"
        })
        token = response.data.get('token') #WE GET THE TOKEN
        print(f'Token to Sharon testing database superuser delete {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #PASS ITS CREDENTIALS HERE
        #we get the database here
        database = Database.objects.get(database_name='Literature')
        database_id = database.id
        self.database_detail_url = reverse('database-detail',args=[database_id])
        response = self.client.delete(self.database_detail_url)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
        print(f'Response data check after superuser deletes database trial {response.data}') 
        
#............................................
#............................................
#............................................
#TEST BOOK CRUD OPERATIONS
    """
    Test create book
    """
    def test_create_book_by_student(self):
        #first, we test if a student without necessary permissions can create a book
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token')
        print(f'Token to Rashan testing book student creation {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id create book: {database_id}")
        response = self.client.post(self.books_url,{
            "title":"Mythical Philosophy",
            "author":"Jackie,Newman",
            "isbn":"8741762779715",
            "published_date":"2010-11-01",
            "number_of_copies":3,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after student tries to creates book {response.data}') #response data prints an error
     
    def test_create_book_by_admin(self):
        #first, we test if an admin has  necessary permissions can create a book
        response = self.client.post(self.login_url,{
            "email":"yasmin@gmail.com",
            "password":"yAsming34t"
        })
        token = response.data.get('token')
        print(f'Token to Yasmin testing book admin creation {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id create book by admin: {database_id}")
        response = self.client.post(self.books_url,{
            "title":"Miseducation of the Black Man",
            "author":"Jackie, Newman",
            "isbn":"8791766859718",
            "published_date":"2010-11-01",
            "number_of_copies":3,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        print(f'Response data check after admin tries to creates book {response.data}') #response data shows a book is created
    """
    Test update book
    """
    def test_update_book_by_student(self):
        #I'm checking whether a student is prevented from updating a book instance
         #first, login in the student
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token')
        print(f'Token for Rashan testing book student update {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #with authenticate with a token
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id update book by student: {database_id}")
        book = Book.objects.get(title="Mythical Philosophy 2")
        self.books_detail_url = reverse('books-detail',args=[book.id]) #we create a new detail url
        response = self.client.put(self.books_detail_url,{
            "title":"Mythical Philosophy 2",
            "author":"James,John",
            "isbn":"8741762779715",
            "published_date":"2010-11-01",
            "number_of_copies":3,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN)
        print(f'Response data check after student tries to update book {response.data}')
    def test_update_book_by_admin(self):
        #here, I want to check whether a student is prevented from updating a book instance
         #first, login in the student
        response = self.client.post(self.login_url,{
            "email":"yasmin@gmail.com",
            "password":"yAsming34t"
        })
        token = response.data.get('token')
        print(f'Token for Yasmin testing book admin update {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #with authenticate with a token
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id update book by admin: {database_id}")
        book = Book.objects.get(title="Mythical Philosophy 3")
        self.books_detail_url = reverse('books-detail',args=[book.id]) #we create a new detail url
        response = self.client.put(self.books_detail_url,{
            "title":"Mythical Philosophy 3",
            "author":"Jackie, Newman",
            "isbn":"8741762779715",
            "published_date":"2010-11-01",
            "number_of_copies":3,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(f'Response data check after admin tries to update book {response.data}')
    """
    test delete book
    """
    def test_delete_book_by_student(self):
        #here, I want to check whether a student is prevented from updating a book instance
         #first, login in the student
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token')
        print(f'Token for Rasha testing book student delete {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #with authenticate with a token
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id delete book by student: {database_id}")
        book = Book.objects.get(title="Mythical Philosophy")
        self.books_delete_url = reverse('books-detail',args=[book.id]) #we create a new detail url
        response = self.client.delete(self.books_delete_url)
        self.assertEquals(response.status_code,status.HTTP_403_FORBIDDEN) #we expect this error because student is forbidden
        print(f'Response data check after student tries to delete book {response.data}')
    def test_delete_book_by_admin(self):
        #here, I want to check whether a student is prevented from updating a book instance
         #first, login in the student
        response = self.client.post(self.login_url,{
            "email":"yasmin@gmail.com",
            "password":"yAsming34t"
        })
        token = response.data.get('token')
        print(f'Token for Yasmin testing book admin delete {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #with authenticate with a token
        #we must get the database
        database = Database.objects.get(database_name='History')
        database_id = database.id
        print(f"database id delete book by admin: {database_id}")
        book = Book.objects.get(title="Mythical Philosophy")
        self.books_delete_url = reverse('books-detail',args=[book.id]) #we create a new detail url
        response = self.client.delete(self.books_delete_url)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
        print(f'Response data check after admin tries to delete book {response.data}')
    """
    test Read
    """
    def test_student_read(self):
        #first, we test whether a regular user can see the the books present
        response = self.client.post(self.login_url,{
            "email":"rasha@gmail.com",
            "password":"rasha1t123"
        })
        token = response.data.get('token')
        print(f'Token to Rashan testing book student Read {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #details are passed using credentials
        response = self.client.get(self.books_url)
        self.assertEquals(response.status_code,status.HTTP_200_OK) #allows us to check whether the status code is the same
        print(f'Response data check if student can see available books {response.data}') #print function is used as a test to see what data is printed out