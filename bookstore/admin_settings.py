# Django Admin Settings Configuration
from django.db import models
from django.contrib import admin

class StoreSettings(models.Model):
    """Store settings for contact and social media"""
    store_email = models.EmailField(max_length=254, help_text="Store contact email address")
    facebook_url = models.URLField(max_length=500, blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(max_length=500, blank=True, help_text="Twitter profile URL")
    whatsapp_url = models.URLField(max_length=500, blank=True, help_text="WhatsApp contact URL")
    
    class Meta:
        verbose_name = "Store Settings"
        verbose_name_plural = "Store Settings"
    
    def __str__(self):
        return f"Store Settings - {self.store_email}"

@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    list_display = ['store_email', 'facebook_url', 'twitter_url', 'whatsapp_url']
    
    def has_add_permission(self, request):
        # Only allow one instance of settings
        return not self.model.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
