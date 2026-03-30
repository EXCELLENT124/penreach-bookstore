from .models import WishList

def wishlist(request):
    """Context processor to add wishlist count to all templates."""
    if request.user.is_authenticated:
        wishlist_count = WishList.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    
    return {'wishlist_count': wishlist_count}
