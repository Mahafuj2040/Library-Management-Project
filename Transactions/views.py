from django.shortcuts import render, redirect, get_object_or_404
from .models import Transactions, BorrowedBook, Book
from .forms import DepositForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from Users.models import Profile
from django.contrib import messages
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

@login_required
def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'deposit'
            profile = request.user.profile
            profile.balance += transaction.amount
            transaction.balance_after_transaction = profile.balance
            profile.save()
            transaction.save()
            messages.success(request, "You have successfully deposited your money.")
            send_transaction_email(
                request.user, 
                transaction.amount, 
                "Deposit Confirmation", 
                'Transactions/deposit_email.html'
            )
            return redirect('profile')
    else:
        form = DepositForm()
    return render(request, 'Transactions/deposit.html', {'form': form})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile, created = Profile.objects.get_or_create(user=request.user)

    borrowed_book = BorrowedBook.objects.filter(user=request.user, book=book, returned=False).first()

    if borrowed_book:
        messages.info(request, "You have already borrowed this book.")
        return redirect('profile')
    
    if profile.balance >= book.borrowing_price:
        profile.balance -= book.borrowing_price
        profile.save()

        borrowed_book = BorrowedBook.objects.create(user=request.user, book=book)

        transaction = Transactions.objects.create(
            user=request.user,
            transaction_type='borrow',
            amount=book.borrowing_price,
            book=book,
            balance_after_transaction=profile.balance
        )
        
        messages.success(request, "You have successfully borrowed the book.")
        send_transaction_email(
            request.user,
            book.borrowing_price,
            "Borrowing Confirmation",
            'Transactions/borrow_email.html'
        )
        
        return redirect('profile')
    else:
        messages.error(request, "You have insufficient balance to borrow the book.")
        send_transaction_email(
            request.user,
            0,
            "Borrowing Failed",
            'Transactions/borrow_failed_email.html'
        )
        return redirect('profile')


@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
    profile = request.user.profile
    
    if not borrowed_book.returned:
        profile.balance += borrowed_book.book.borrowing_price
        profile.save()
        borrowed_book.returned = True
        borrowed_book.save()
        transaction = Transactions.objects.create(
            user=request.user,
            transaction_type='return',
            amount=borrowed_book.book.borrowing_price,
            book=borrowed_book.book,
            balance_after_transaction=profile.balance
        )
        messages.success(request, "Your book has been returned, and your money is added to your account.")
        send_transaction_email(
            request.user, 
            borrowed_book.book.borrowing_price, 
            "Return Confirmation", 
            'Transactions/return_email.html'
        )
        
    return redirect('profile')
