from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from books.models import Book
from .models import Cart, CartItem
from django.views.decorators.http import require_POST

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to add product to cart')
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{book.title} added to cart!')
    return redirect('cart_view')

def cart_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your cart')
        return redirect('login')
    
    # Get all active cart items for the user
    cart_items = CartItem.objects.filter(user=request.user, is_active=True).select_related('book')
    
    # Merge duplicate items (same book) into single entry
    merged_items = {}
    for item in cart_items:
        if item.book_id in merged_items:
            # Merge quantities and update the existing item
            existing = merged_items[item.book_id]
            existing.quantity += item.quantity
            existing.save()
            # Delete the duplicate
            item.delete()
        else:
            merged_items[item.book_id] = item
    
    # Convert back to list
    cart_items = list(merged_items.values())
    
    total = sum(item.sub_total() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'total_items': total_items
    }
    return render(request, 'cart/cart.html', context)

@require_POST
def update_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to update your cart')
        return redirect('login')
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to remove items from your cart')
        return redirect('login')
    
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart_view')
