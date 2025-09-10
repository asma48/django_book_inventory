from django.db import models

# Create your models here.



class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    discription = models.CharField(max_length=500)
    isbn = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')