# Bookstore models
from django.db import models

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
