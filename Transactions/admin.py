from django.contrib import admin
from .models import Transactions, BorrowedBook
# Register your models here.

admin.site.register(Transactions)
admin.site.register(BorrowedBook)
