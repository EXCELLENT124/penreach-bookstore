from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from books.models import Book

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book_title', 'book_author', 'price', 'quantity', 'sub_total')
    fields = ('book_title', 'book_author', 'price', 'quantity', 'sub_total')
    
    def sub_total(self, obj):
        try:
            return f"R {obj.sub_total():.2f}"
        except (TypeError, ValueError):
            return "R 0.00"
    sub_total.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'phone', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def _update_stock_for_order(self, order, request):
        """
        Subtract stock from books when order is being processed.
        Returns tuple of (success_count, error_messages)
        """
        errors = []
        success_count = 0
        
        with transaction.atomic():
            for item in order.items.all():
                try:
                    # Find the book by title (and optionally author)
                    book = Book.objects.filter(
                        title__iexact=item.book_title,
                        is_active=True
                    ).first()
                    
                    if not book:
                        errors.append(f"Book '{item.book_title}' not found in inventory")
                        continue
                    
                    # Check if there's enough stock
                    if book.stock < item.quantity:
                        errors.append(
                            f"Insufficient stock for '{item.book_title}'. "
                            f"Available: {book.stock}, Required: {item.quantity}"
                        )
                        continue
                    
                    # Subtract stock
                    book.stock -= item.quantity
                    book.save()
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Error updating stock for '{item.book_title}': {str(e)}")
        
        return success_count, errors
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected orders as confirmed'
    
    def mark_as_processing(self, request, queryset):
        """Mark orders as processing and subtract stock from inventory"""
        processed_count = 0
        error_messages = []
        
        for order in queryset:
            if order.status in ['pending', 'confirmed']:
                # Only subtract stock if not already processed
                success_count, errors = self._update_stock_for_order(order, request)
                
                if errors:
                    error_messages.extend(errors)
                
                if success_count > 0 or not errors:
                    order.status = 'processing'
                    order.save()
                    processed_count += 1
            else:
                error_messages.append(
                    f"Order {order.order_number} is already {order.status}. "
                    "Stock was not subtracted again."
                )
                # Still update status if needed
                if order.status != 'processing':
                    order.status = 'processing'
                    order.save()
                    processed_count += 1
        
        # Display results
        if processed_count > 0:
            self.message_user(
                request, 
                f'{processed_count} order(s) marked as processing. Stock has been subtracted from inventory.',
                messages.SUCCESS
            )
        
        if error_messages:
            for error in error_messages:
                self.message_user(request, error, messages.WARNING)
    
    mark_as_processing.short_description = 'Mark selected orders as processing (subtracts stock)'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f'{queryset.count()} order(s) marked as shipped.')
    mark_as_shipped.short_description = 'Mark selected orders as shipped'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f'{queryset.count()} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book_title', 'book_author', 'price', 'quantity', 'sub_total')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('book_title', 'book_author', 'order__order_number', 'order__full_name')
    readonly_fields = ('sub_total',)
    ordering = ('-order__created_at',)
    
    def sub_total(self, obj):
        try:
            return f"R {obj.sub_total():.2f}"
        except (TypeError, ValueError):
            return "R 0.00"
    sub_total.short_description = 'Subtotal'
