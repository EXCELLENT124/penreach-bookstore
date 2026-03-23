# Context processor for store settings
from .models import StoreSettings

def store_settings(request):
    """Make store settings available in templates"""
    try:
        settings = StoreSettings.objects.first()
        return {
            'store_email': settings.store_email if settings else '',
            'facebook_url': settings.facebook_url if settings else '',
            'twitter_url': settings.twitter_url if settings else '',
            'whatsapp_url': settings.whatsapp_url if settings else '',
        }
    except:
        return {
            'store_email': '',
            'facebook_url': '',
            'twitter_url': '',
            'whatsapp_url': '',
        }
