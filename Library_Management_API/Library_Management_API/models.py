from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_isbn(value):
    # Add more robust ISBN validation if needed (e.g., check length and format)
    if len(value) != 13:
        raise ValidationError("ISBN must be 13 digits long.")

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, validators=[validate_isbn])
    published_date = models.DateField()
    copies_available = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.return_date:
            book = self.book
            book.copies_available += 1
            book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} checked out {self.book.title}"
