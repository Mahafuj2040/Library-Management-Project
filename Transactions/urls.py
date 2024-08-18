
from django.urls import path, include
from .views import deposit_money, borrow_book,return_book

urlpatterns = [
    path('deposit_money/', deposit_money, name='deposit_money'), 
    path('borrow_book/<int:book_id>/', borrow_book, name='borrow_book'), 
    path('return_book/<int:borrowed_book_id>/', return_book, name='return_book'),
]
