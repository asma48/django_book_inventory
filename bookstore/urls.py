from django.contrib import admin
from django.urls import include, path
from django.views import View
from app.views import  BookView, UserView, BookList, Books, Users
from rest_framework.routers import DefaultRouter


book = BookView()
user = UserView()
router = DefaultRouter()

router.register('user', Users, basename='User')
router.register('book', Books, basename='Book')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/<int:pk>', book.book_detail),
    path('book/create/', book.book_create),
    path('book/search/', book.book),
    path('book/list/', BookList.as_view()),
    path('book/update/', book.book_update),
    path('book/delete/', book.book_delete),
    path('user/signup/', user.user_create),
    path('user/login/', user.log_in),
    path('', include(router.urls)),
    
]

