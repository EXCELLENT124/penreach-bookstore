from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import Book
import csv
import io
from PIL import Image
import os
from django.core.files.base import ContentFile
import uuid

class BookBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with book information. Columns: title, author, description, price, isbn, publisher, publication_date, pages, language, stock, book_type'
    )
    images_zip = forms.FileField(
        label='Images ZIP File (Optional)',
        required=False,
        help_text='Upload a ZIP file containing cover images. Images should be named with ISBN or title.'
    )

@method_decorator(csrf_protect)
def bulk_upload_view(request):
    if request.method == 'POST':
        form = BookBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            images_zip = request.FILES.get('images_zip')
            
            # Process CSV
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            
            # Process images if provided
            images = {}
            if images_zip:
                import zipfile
                with zipfile.ZipFile(images_zip) as zip_file:
                    for file_info in zip_file.infolist():
                        if file_info.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            image_data = zip_file.read(file_info.filename)
                            # Store image data with filename as key
                            images[file_info.filename.lower()] = image_data
            
            created_count = 0
            updated_count = 0
            errors = []
            
            for row in csv_reader:
                try:
                    # Prepare book data
                    book_data = {
                        'title': row.get('title', '').strip(),
                        'author': row.get('author', '').strip(),
                        'description': row.get('description', '').strip(),
                        'price': float(row.get('price', 0)),
                        'isbn': row.get('isbn', '').strip(),
                        'publisher': row.get('publisher', '').strip(),
                        'publication_date': row.get('publication_date', '2023-01-01'),
                        'pages': int(row.get('pages', 0)),
                        'language': row.get('language', 'English'),
                        'stock': int(row.get('stock', 0)),
                        'book_type': row.get('book_type', 'small_books'),
                    }
                    
                    # Find matching image
                    cover_image = None
                    if images:
                        # Try to match by ISBN first, then by title
                        isbn_match = f"{book_data['isbn']}.jpg"
                        title_match = f"{book_data['title'].lower()}.jpg"
                        
                        for img_filename, img_data in images.items():
                            if (isbn_match in img_filename.lower() or 
                                title_match in img_filename.lower() or
                                book_data['isbn'] in img_filename or
                                book_data['title'].lower() in img_filename.lower()):
                                
                                # Create image file
                                image_name = f"book_cover_{uuid.uuid4()}.jpg"
                                cover_image = ContentFile(img_data, name=image_name)
                                break
                    
                    # Create or update book
                    book, created = Book.objects.update_or_create(
                        isbn=book_data['isbn'],
                        defaults=book_data
                    )
                    
                    if cover_image:
                        book.cover_image = cover_image
                        book.save()
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except Exception as e:
                    errors.append(f"Error processing row: {row.get('title', 'Unknown')} - {str(e)}")
            
            messages.success(request, f'Successfully created {created_count} books and updated {updated_count} books.')
            if errors:
                messages.warning(request, f'Encountered {len(errors)} errors. See details below.')
                for error in errors[:10]:  # Show first 10 errors
                    messages.error(request, error)
            
            return redirect('admin:books_book_changelist')
    else:
        form = BookBulkUploadForm()
    
    context = {
        'form': form,
        'title': 'Bulk Upload Books',
        'opts': Book._meta,
        'has_change_permission': True,
        'has_add_permission': True,
    }
    
    return render(request, 'admin/books/bulk_upload.html', context)

class BookAdmin(admin.ModelAdmin):
    # Custom template for enhanced book list with preview
    change_list_template = 'admin/books/book/change_list.html'
    
    list_display = ('title', 'author', 'book_type', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'language', 'publisher', 'book_type')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('price', 'stock', 'is_active', 'book_type')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'description', 'book_type')
        }),
        ('Publication Details', {
            'fields': ('publisher', 'publication_date', 'pages', 'language')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_draft', 'bulk_publish_drafts']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(bulk_upload_view), name='books_book_bulk_upload'),
        ]
        return custom_urls + urls
    
    def mark_as_draft(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=False)
        self.message_user(request, f'{updated} books marked as draft.')
    mark_as_draft.short_description = 'Mark selected books as draft'
    
    def bulk_publish_drafts(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f'{updated} draft books published.')
    bulk_publish_drafts.short_description = 'Publish selected draft books'
