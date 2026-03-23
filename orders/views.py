from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import CartItem
from cart.views import _cart_id

@login_required
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart_id = _cart_id(request)
        from cart.models import Cart
        cart = Cart.objects.filter(cart_id=cart_id).first()
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) if cart else CartItem.objects.none()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart_view')
    
    total = sum(item.sub_total() for item in cart_items)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.total_amount = total
                if request.user.is_authenticated:
                    order.user = request.user
                    order.full_name = request.user.full_name
                    order.email = request.user.email
                    order.phone = request.user.phone
                    order.address = request.user.address
                order.save()
                
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        book_title=item.book.title,
                        book_author=item.book.author,
                        price=item.book.price,
                        quantity=item.quantity
                    )
                    item.delete()
                
                # Send order confirmation email
                try:
                    email_subject = f'Order Confirmation - {order.order_number}'
                    email_body = render_to_string('orders/order_confirmation_email.txt', {
                        'order': order,
                    })
                    send_mail(
                        subject=email_subject,
                        message=email_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[order.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Log the error but don't prevent order completion
                    print(f"Failed to send order confirmation email: {e}")
                
                messages.success(request, f'Order placed successfully! Your order number is {order.order_number}')
                return redirect('order_confirmation', order_id=order.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.full_name,
                'email': request.user.email,
                'phone': request.user.phone,
                'address': request.user.address,
            }
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'total_items': sum(item.quantity for item in cart_items)
    }
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.user and order.user != request.user:
        return redirect('home')
    
    context = {
        'order': order
    }
    return render(request, 'orders/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'orders/order_history.html', context)
