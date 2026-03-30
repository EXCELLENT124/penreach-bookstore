from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg
from .models import Visitor, DailyStats, PageView


@staff_member_required
def analytics_dashboard(request):
    """Dashboard view for website analytics"""
    
    # Get date ranges
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # Today's stats
    today_stats = DailyStats.objects.filter(date=today).first()
    
    # Yesterday's stats
    yesterday_stats = DailyStats.objects.filter(date=yesterday).first()
    
    # Total stats
    total_visits = DailyStats.objects.aggregate(total=Count('total_visits'))['total'] or 0
    total_unique = DailyStats.objects.aggregate(total=Count('unique_visitors'))['total'] or 0
    
    # Recent visitors (last 24 hours)
    recent_visitors = Visitor.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-timestamp')[:50]
    
    # Daily stats for the last 7 days (for chart)
    weekly_stats = DailyStats.objects.filter(date__gte=last_7_days).order_by('date')
    
    # Monthly stats (last 30 days)
    monthly_stats = DailyStats.objects.filter(date__gte=last_30_days).order_by('date')
    
    # Top pages
    top_pages = PageView.objects.order_by('-view_count')[:10]
    
    # Total unique visitors count (approximate)
    unique_visitor_count = Visitor.objects.values('ip_address').distinct().count()
    
    context = {
        'today_stats': today_stats,
        'yesterday_stats': yesterday_stats,
        'total_visits': total_visits,
        'total_unique_visitors': unique_visitor_count,
        'recent_visitors': recent_visitors,
        'weekly_stats': weekly_stats,
        'monthly_stats': monthly_stats,
        'top_pages': top_pages,
        'today': today,
    }
    
    return render(request, 'analytics/dashboard.html', context)
