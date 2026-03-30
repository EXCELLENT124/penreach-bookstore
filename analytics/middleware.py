import uuid
from django.utils import timezone
from django.db.models import F
from .models import Visitor, DailyStats, PageView


class VisitorTrackingMiddleware:
    """Middleware to track website visitors and page views"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Don't track admin pages, static files, or media files
        path = request.path
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        
        # Get or create session key
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Get referrer
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Check if this is a unique visitor (no record in last 24 hours for this IP/session)
        is_unique = False
        last_visit = Visitor.objects.filter(
            ip_address=ip,
            timestamp__date=timezone.now().date()
        ).first()
        
        if not last_visit:
            is_unique = True
        
        # Create visitor record
        Visitor.objects.create(
            ip_address=ip,
            user_agent=user_agent[:500] if user_agent else '',
            referrer=referrer[:200] if referrer else '',
            page_visited=path[:255],
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None,
            is_unique=is_unique
        )
        
        # Update daily stats
        today = timezone.now().date()
        daily_stats, created = DailyStats.objects.get_or_create(
            date=today,
            defaults={
                'total_visits': 1,
                'unique_visitors': 1 if is_unique else 0,
                'registered_users_visits': 1 if request.user.is_authenticated else 0
            }
        )
        
        if not created:
            daily_stats.total_visits = F('total_visits') + 1
            if is_unique:
                daily_stats.unique_visitors = F('unique_visitors') + 1
            if request.user.is_authenticated:
                daily_stats.registered_users_visits = F('registered_users_visits') + 1
            daily_stats.save()
        
        # Update page view count - handle potential duplicates
        try:
            page_view, created = PageView.objects.get_or_create(
                page_path=path[:255],
                defaults={
                    'page_name': self._get_page_name(path),
                    'view_count': 1
                }
            )
            
            if not created:
                page_view.view_count = F('view_count') + 1
                page_view.save()
        except PageView.MultipleObjectsReturned:
            # If duplicates exist, use the first one and increment it
            page_view = PageView.objects.filter(page_path=path[:255]).first()
            if page_view:
                page_view.view_count = F('view_count') + 1
                page_view.save()
                # Clean up duplicates
                PageView.objects.filter(page_path=path[:255]).exclude(pk=page_view.pk).delete()
        
        response = self.get_response(request)
        return response
    
    def _get_page_name(self, path):
        """Generate a friendly page name from path"""
        if path == '/':
            return 'Home'
        elif path.startswith('/books/'):
            return 'Books'
        elif path.startswith('/cart/'):
            return 'Cart'
        elif path.startswith('/checkout/'):
            return 'Checkout'
        elif path.startswith('/orders/'):
            return 'Orders'
        elif path.startswith('/wishlist/'):
            return 'Wishlist'
        elif path.startswith('/accounts/'):
            return 'Account'
        elif path.startswith('/contact/'):
            return 'Contact'
        elif path.startswith('/about/'):
            return 'About'
        return path.split('/')[-1].replace('-', ' ').title() or 'Page'
