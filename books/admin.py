from django.contrib import admin
from .models import Book
from .admin_bulk_upload import BookAdmin

admin.site.register(Book, BookAdmin)
