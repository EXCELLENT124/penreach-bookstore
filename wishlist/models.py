from django.db import models
from django.conf import settings
from books.models import Book

class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlist_items')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'wishlist'
        unique_together = ['user', 'book']  # Prevent duplicate wish list items
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.book.title}"
