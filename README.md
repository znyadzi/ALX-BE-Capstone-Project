---

# Library Management System API

### Overview
This is a **Library Management System API** built using **Django** and **Django REST Framework (DRF)**. The API manages library resources, including books and users, and provides endpoints for users to borrow and return books. The project emphasizes backend development, database management, and API design to simulate a real-world library management system.

### Key Features:
- **Books Management (CRUD)**: Create, Read, Update, and Delete operations for books in the library.
- **User Management (CRUD)**: Manage library users with a unique username, email, and membership status.
- **Check-Out & Return Books**: Users can check out and return books. The system tracks availability and logs check-out and return dates.
- **View Available Books**: View and filter available books by title, author, or ISBN.
- **Authentication**: Basic authentication for users and optional token-based authentication using JWT.

---

### Functional Requirements

#### Books Management (CRUD):
- **Attributes**: Each book has a `Title`, `Author`, `ISBN`, `Published Date`, and `Number of Copies Available`.
- **Validations**: ISBN numbers must be unique.

#### Users Management (CRUD):
- Manage library users with the following attributes: `Username`, `Email`, `Date of Membership`, and `Active Status`.

#### Book Check-Out & Return:
- Users can check out one book at a time (if copies are available).
- The number of available copies decreases when a book is checked out and increases when returned.
- A log is kept for each check-out and return event, including dates.

#### View Available Books:
- Endpoint to view all available books.
- Searchable by `Title`, `Author`, or `ISBN`.
- Filters to only show books with available copies.

---

### Technical Requirements

#### 1. **Database**
- Utilizes **Django ORM** to interact with the database.
- Three main models: `Books`, `Users`, and `Transactions` (to track book check-outs and returns).

#### 2. **Authentication**
- Basic user authentication using Django’s built-in system.
- Token-based authentication using JWT for enhanced security (optional).
- Users can log in and access their borrowing history.

#### 3. **API Design**
- Built with **Django REST Framework (DRF)**.
- RESTful principles followed (e.g., `GET`, `POST`, `PUT`, `DELETE` requests).
- Proper error handling with appropriate HTTP status codes.

---

### Setup Instructions

#### 1. **Requirements**
- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL or any other database supported by Django

#### 2. **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/library-management-api.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup your database in the `settings.py` file:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

#### 3. **Running the Server**
To start the development server:
```bash
python manage.py runserver
```

#### 4. **Superuser Creation**
To create an admin superuser for accessing the Django admin panel:
```bash
python manage.py createsuperuser
```

---

### API Endpoints

#### **Books**
- **GET /books/**: List all books or filter by availability.
- **POST /books/**: Add a new book.
- **PUT /books/{id}/**: Update an existing book.
- **DELETE /books/{id}/**: Remove a book.

#### **Users**
- **GET /users/**: List all users.
- **POST /users/**: Register a new user.
- **PUT /users/{id}/**: Update a user’s information.
- **DELETE /users/{id}/**: Remove a user.

#### **Check-Out/Return Books**
- **POST /books/{id}/checkout/**: Check out a book.
- **POST /books/{id}/return/**: Return a checked-out book.

#### **Authentication**
- **POST /auth/login/**: User login (optional JWT).
- **GET /users/{id}/history/**: View user’s borrowing history.

---

### Deployment

This API can be deployed on **Heroku**, **PythonAnywhere**, or any other cloud platform.

1. Push the code to a remote repository (GitHub, GitLab).
2. Deploy the application by connecting the repository to Heroku.
3. Ensure environment variables (such as database credentials) are set in the deployment environment.

For detailed deployment instructions on Heroku:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku master
```

---

### Future Enhancements

- Add **role-based access control** (admin, librarian, member).
- Implement **fines** for overdue book returns.
- Extend **reporting capabilities** (most borrowed books, active users, etc.).

---

### License
This project is licensed under the MIT License.

---

### Contact
For any questions or feedback, please reach out at **znyadzi1@gmail.com**.

---

This README provides an organized structure for users and developers to understand, setup, and extend the Library Management API
