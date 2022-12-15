from .models import Cart

def delete_old_carts():
    """
    Delete cart after 30 days
    """
    for cart in  Cart.objects.all():
        if cart.can_be_deleted:
            cart.delete()
    