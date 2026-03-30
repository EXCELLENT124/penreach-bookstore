from django.contrib import admin
from .models import Visitor, DailyStats, PageView


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'page_visited', 'timestamp', 'user', 'is_unique']
    list_filter = ['timestamp', 'is_unique', 'page_visited']
    search_fields = ['ip_address', 'user_agent', 'page_visited']
    readonly_fields = ['ip_address', 'user_agent', 'referrer', 'page_visited', 
                       'session_key', 'timestamp', 'is_unique', 'user']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_visits', 'unique_visitors', 'registered_users_visits']
    list_filter = ['date']
    readonly_fields = ['date', 'total_visits', 'unique_visitors', 'registered_users_visits']
    ordering = ['-date']
    
    def has_add_permission(self, request):
        return False


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'page_path', 'view_count', 'last_viewed']
    list_filter = ['last_viewed']
    search_fields = ['page_name', 'page_path']
    readonly_fields = ['page_path', 'view_count', 'last_viewed']
    ordering = ['-view_count']
