from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from Transactions.models import BorrowedBook, Transactions

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Congratulations! Your Account was Created Successfully.")
                return redirect('profile')
        else:
            form = RegisterForm()
        return render(request, 'Users/signup.html', {'form': form})
    else:
        return redirect('profile')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                user = authenticate(username=name, password=user_pass)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid username or password.')
        else:
            form = AuthenticationForm()
        return render(request, 'Users/login.html', {'form': form})  
    else:
        return redirect('profile')

@login_required
def profile(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    transactions = Transactions.objects.filter(user=request.user)
    
    context = {
        'borrowed_books' : borrowed_books,
        'transactions' : transactions
    }
    
    return render(request, 'Users/profile.html', context)

@login_required
def change_data(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Updated Successfully')
            return redirect('profile')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'Users/update_data.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('user_login')

@login_required
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "Password Changed Successfully")
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'Users/passChange.html', {'form': form})  
