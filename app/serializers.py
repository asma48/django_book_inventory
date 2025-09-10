from rest_framework import serializers
from .models import Book, User
from django.contrib.auth.hashers import make_password


    
class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Weak Password')
        return value

    def validate(self, data):
        nm = data.get('name')
        pwd = data.get('password')
        if nm.lower() == 'asmaali' and pwd.lower() == 'asma1234':
            raise serializers.ValidationError('Can not use this name and password')
        else:
            return data
        


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn','discription']




class UserSerial(serializers.ModelSerializer):
    book = serializers.StringRelatedField(many= True, read_only = True)
    class Meta:
        model = Book
        fields = ['id', 'name', 'email']


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     author = serializers.CharField()
#     isbn = serializers.IntegerField()
#     discription = serializers.CharField()

#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.author = validated_data.get('author', instance.author)
#         instance.isbn = validated_data.get('isbn', instance.isbn)
#         instance.discription = validated_data.get('discription', instance.discription)
#         instance.save()
#         return instance
    