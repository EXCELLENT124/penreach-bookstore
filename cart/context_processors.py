from .models import CartItem, Cart

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        cart_count = sum(item.quantity for item in cart_items)
    else:
        cart_items = CartItem.objects.none()
        cart_count = 0
    
    return {'cart': cart_items, 'cart_count': cart_count}
