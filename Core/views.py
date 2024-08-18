from django.shortcuts import render
from Users.models import Profile
from Transactions.models import BorrowedBook, Transactions

def home(request):
    if request.user.is_authenticated:
        borrowed_books = BorrowedBook.objects.filter(user=request.user)
        transactions = Transactions.objects.filter(user=request.user)
        context = {
            'borrowed_books': borrowed_books,
            'transactions': transactions
        }
    else:
        context = {}
    return render(request, 'base.html', context)
