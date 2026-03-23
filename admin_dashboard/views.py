from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from orders.models import Order, OrderItem
from accounts.models import CustomUser

@staff_member_required
def dashboard(request):
    # Get date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    # Basic counts
    total_books = Book.objects.count()
    total_orders = Order.objects.count()
    total_customers = CustomUser.objects.count()
    active_books = Book.objects.filter(is_active=True).count()
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Orders statistics
    orders_last_7_days = Order.objects.filter(created_at__date__gte=last_7_days).count()
    orders_last_30_days = Order.objects.filter(created_at__date__gte=last_30_days).count()
    
    # Revenue statistics
    revenue_last_7_days = Order.objects.filter(
        created_at__date__gte=last_7_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_last_30_days = Order.objects.filter(
        created_at__date__gte=last_30_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order status breakdown
    order_status_counts = Order.objects.values('status').annotate(count=Count('status'))
    
    # Top selling books
    top_books = OrderItem.objects.values('book_title', 'book_author').annotate(
        total_sold=Sum('quantity'),
        revenue=Sum('price') * Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    # Low stock books
    low_stock_books = Book.objects.filter(stock__lt=10, is_active=True).order_by('stock')[:5]
    
    context = {
        'total_books': total_books,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'active_books': active_books,
        'recent_orders': recent_orders,
        'orders_last_7_days': orders_last_7_days,
        'orders_last_30_days': orders_last_30_days,
        'revenue_last_7_days': revenue_last_7_days,
        'revenue_last_30_days': revenue_last_30_days,
        'total_revenue': total_revenue,
        'order_status_counts': order_status_counts,
        'top_books': top_books,
        'low_stock_books': low_stock_books,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)
