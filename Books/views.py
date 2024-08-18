from django.shortcuts import render, get_object_or_404
from .models import Book, Category, Review
from .forms import ReviewForm


def book_list(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        books = books.filter(categories__name=selected_category)
    context = {'books': books, 'categories': categories, 'selected_category': selected_category}
    return render(request, 'Books/book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
    else:
        form = ReviewForm()
    context = {'book': book, 'reviews': reviews, 'form': form}
    return render(request, 'Books/book_detail.html', context)
