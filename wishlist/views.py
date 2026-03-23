from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from books.models import Book
from .models import WishList

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is already in wishlist
    if WishList.objects.filter(user=request.user, book=book).exists():
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Book is already in your wishlist'})
        else:
            messages.warning(request, f'"{book.title}" is already in your wishlist')
    else:
        # Add to wishlist
        WishList.objects.create(user=request.user, book=book)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Book added to wishlist'})
        else:
            messages.success(request, f'"{book.title}" added to your wishlist')
    
    # Redirect back or return JSON for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Book added to wishlist'})
    
    return redirect(request.META.get('HTTP_REFERER', 'book_list'))

@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    try:
        wishlist_item = WishList.objects.get(user=request.user, book=book)
        wishlist_item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Book removed from wishlist'})
        else:
            messages.success(request, f'"{book.title}" removed from your wishlist')
    except WishList.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Book not found in wishlist'})
        else:
            messages.error(request, 'Book not found in your wishlist')
    
    # Redirect back or return JSON for AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Book removed from wishlist'})
    
    return redirect(request.META.get('HTTP_REFERER', 'book_list'))

@login_required
def wishlist_view(request):
    wishlist_items = WishList.objects.filter(user=request.user).select_related('book')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context)

@login_required
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is already in wishlist
    wishlist_item = WishList.objects.filter(user=request.user, book=book).first()
    
    if wishlist_item:
        # Remove from wishlist
        wishlist_item.delete()
        in_wishlist = False
        message = f'"{book.title}" removed from wishlist'
    else:
        # Add to wishlist
        WishList.objects.create(user=request.user, book=book)
        in_wishlist = True
        message = f'"{book.title}" added to wishlist'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'in_wishlist': in_wishlist,
            'message': message
        })
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'book_list'))
