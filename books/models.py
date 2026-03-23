from django.db import models

class Book(models.Model):
    BOOK_TYPES = [
        ('small_books', 'Small Books'),
        ('charts', 'Charts'),
        ('big_books', 'Big Books'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=100)
    publication_date = models.DateField()
    pages = models.IntegerField()
    language = models.CharField(max_length=50, default='English')
    stock = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES, default='small_books')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author}"
