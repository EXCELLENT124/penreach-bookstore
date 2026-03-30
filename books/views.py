from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Book

@login_required
def profile(request):
    """Display user profile details."""
    user = request.user
    context = {
        'user': user,
        'full_name': user.full_name if hasattr(user, 'full_name') else user.username,
        'email': user.email,
        'phone': getattr(user, 'phone', ''),
        'address': getattr(user, 'address', ''),
    }
    return render(request, 'books/profile.html', context)

@login_required
def edit_profile(request):
    """Allow user to edit profile details."""
    user = request.user
    if request.method == 'POST':
        # Update user profile information
        user.full_name = request.POST.get('full_name', user.full_name if hasattr(user, 'full_name') else '')
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', getattr(user, 'phone', ''))
        user.address = request.POST.get('address', getattr(user, 'address', ''))
        user.save()
        return redirect('profile')
    
    context = {
        'user': user,
        'full_name': user.full_name if hasattr(user, 'full_name') else user.username,
        'email': user.email,
        'phone': getattr(user, 'phone', ''),
        'address': getattr(user, 'address', ''),
    }
    return render(request, 'books/edit_profile.html', context)

def home(request):
    featured_books = Book.objects.filter(is_active=True)[:6]
    context = {
        'featured_books': featured_books
    }
    return render(request, 'books/home.html', context)

def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(is_active=True)
    
    if query:
        # Check if query matches book types
        category_keywords = {
            'small books': 'small_books',
            'small book': 'small_books', 
            'compact': 'small_books',
            'portable': 'small_books',
            'charts': 'charts',
            'chart': 'charts',
            'educational': 'charts',
            'diagrams': 'charts',
            'big books': 'big_books',
            'big book': 'big_books',
            'large': 'big_books',
            'classroom': 'big_books'
        }
        
        # Check for category keywords
        lower_query = query.lower()
        found_category = None
        for keyword, category_type in category_keywords.items():
            if keyword in lower_query:
                found_category = category_type
                break
        
        if found_category:
            # Filter by book type if category keyword found
            try:
                books = books.filter(book_type=found_category)
            except FieldError:
                # If book_type field doesn't exist, fall back to regular search
                books = books.filter(
                    Q(title__icontains=query) | 
                    Q(author__icontains=query) |
                    Q(description__icontains=query)
                )
        else:
            # Regular search
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query) |
                Q(description__icontains=query)
            )
    
    context = {
        'books': books,
        'query': query
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'books/book_detail.html', context)

def category_books(request, category_type):
    books = Book.objects.filter(is_active=True)
    
    # Filter by category type if provided
    if category_type:
        try:
            books = books.filter(book_type=category_type)
        except FieldError:
            # If book_type field doesn't exist, show all books
            books = books
    
    context = {
        'books': books,
        'category_type': category_type,
        'category_display': dict(Book.BOOK_TYPES).get(category_type, 'Unknown Category')
    }
    return render(request, 'books/category_books.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True)
    context = {
        'book': book
    }
    return render(request, 'books/book_detail.html', context)
