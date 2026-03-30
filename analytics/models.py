from django.db import models
from django.conf import settings


class Visitor(models.Model):
    """Model to track website visitors"""
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    page_visited = models.CharField(max_length=255, blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_unique = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class DailyStats(models.Model):
    """Aggregated daily statistics"""
    date = models.DateField(unique=True)
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    registered_users_visits = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Daily Stat'
        verbose_name_plural = 'Daily Stats'
    
    def __str__(self):
        return f"{self.date} - {self.total_visits} visits"


class PageView(models.Model):
    """Track page views"""
    page_path = models.CharField(max_length=255)
    page_name = models.CharField(max_length=100, blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-view_count']
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
    
    def __str__(self):
        return f"{self.page_name or self.page_path} - {self.view_count} views"
