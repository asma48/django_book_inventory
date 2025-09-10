import io
from django.views import View
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Book, User
from .serializers import BookSerializer, UserSerializer, UserSerial
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from app.mypagination import MyPagination



# Create your views here.

def hash_password(password):
    return make_password(password)
def verify_password(password, hashpassword):
    return check_password(password, hashpassword)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserView(View):

    @csrf_exempt
    def user_create(self, request):
        if request.method == 'POST':
            data = request.body
            stream = io.BytesIO(data)
            python_user_obj = JSONParser().parse(stream)

            #if 'password' in python_user_obj:
                #python_user_obj['password'] = hash_password(python_user_obj['password'])
    

            user_data = UserSerializer(data=python_user_obj)

            if user_data.is_valid():
                user_data.save()
                return JsonResponse({'msg': 'User created'})
            
            return JsonResponse(user_data.errors)    

    @csrf_exempt
    def log_in(self, request):
        if request.method == 'POST':  
            data = request.body
            stream = io.BytesIO(data)
            python_user_obj = JSONParser().parse(stream)   

            email = python_user_obj.get("email")
            password = python_user_obj.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password required"}, status=400)

            try:
                db_user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password"}, status=400)
            

            if verify_password(password, db_user.password):
                refresh = RefreshToken.for_user(db_user)
                return JsonResponse({
                    "msg": "User login successful",
                    "user_email": db_user.email,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=400)
            



class BookView(View):

    @csrf_exempt
    def book_create(self, request):
        if request.method == 'POST':
            data = request.body
            stream = io.BytesIO(data)
            python_book_obj = JSONParser().parse(stream)
            book_data = BookSerializer(data=python_book_obj)

            if book_data.is_valid():
                book_data.save()
                return JsonResponse({'msg': 'Book created'})
            
            return JsonResponse(book_data.errors)



    def book(self, request):
        if request.method == 'GET':
            json_data = request.body
            stream = io.BytesIO(json_data)
            book_data = JSONParser().parse(stream)
            book_id = book_data.get('id', None)
            if book_id is not None:
                book = Book.objects.get(id=book_id)
                serializer = BookSerializer(book)
                return JsonResponse(serializer.data, safe=False)
            
            book = Book.objects.all()
            serializer = BookSerializer(book, many=True)
            return JsonResponse(serializer.data, safe=False)


    @csrf_exempt
    def book_update(self, request):
        if request.method == 'PUT':
            json_data = request.body
            stream = io.BytesIO(json_data)
            book_data = JSONParser().parse(stream)
            book_id = book_data.get('id')
            if book_id is not None:
                book = Book.objects.get(id=book_id)
                serializer = BookSerializer(book, data=book_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(data={
                        "message": "Book Updated Successfully",
                        "Book": serializer.data
                    })
            return JsonResponse(serializer.errors)


    @csrf_exempt
    def book_delete(self, request):
        if request.method == 'DELETE':
            json_data = request.body
            stream = io.BytesIO(json_data)
            book_data = JSONParser().parse(stream)
            book_id = book_data.get('id')
            if book_id is not None:
                book = Book.objects.get(id=book_id)
                book.delete()
                return JsonResponse({"message": "Book Deleted Successfully"})



    def book_detail(self, request, pk):
        db_book = Book.objects.get(id=pk)
        book = BookSerializer(db_book)
        json_book = JSONRenderer().render(book.data)
        return JsonResponse(book.data)
    


class BookList(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MyPagination
    




class Books(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class Users(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
