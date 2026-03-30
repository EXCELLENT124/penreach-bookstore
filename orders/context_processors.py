from .models import Order


def user_orders(request):
    """
    Context processor to fetch user's recent orders for order tracking display.
    Returns the 3 most recent orders for authenticated users.
    """
    orders = []
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:3]
    return {
        'user_recent_orders': orders,
    }
