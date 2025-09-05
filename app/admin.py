from django.contrib import admin
from .models import Book, User
# Register your models here.


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['name', 'email', 'password']

@admin.register(Book)
class Book(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'discription']

