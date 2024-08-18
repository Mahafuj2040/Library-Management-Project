from django.db import models
from django.contrib.auth.models import User
from Books.models import Book
from .constants import TRANSACTION_TYPES
# Create your models here.

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.transaction_type} - {self.amount}'

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    
