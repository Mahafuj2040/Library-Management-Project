
from django.urls import path, include
from .views import book_detail, book_list

urlpatterns = [
    path('', book_list, name='book_list'), 
    path('book_detail/<int:book_id>/', book_detail, name='book_detail'), 
]
