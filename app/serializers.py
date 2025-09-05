from rest_framework import serializers
from .models import Book, User


    
class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)



class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    isbn = serializers.IntegerField()
    discription = serializers.CharField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.discription = validated_data.get('discription', instance.discription)
        instance.save()
        return instance
    
