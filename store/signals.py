from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

from .models import Customer,CustomerWishList,Trader


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_customer_wish_list(sender,instance,created,**kwargs):
	if created:
            CustomerWishList.objects.create(customer_id=instance.id)

@receiver(post_save,sender=Customer)
def add_to_customers_group(sender,instance,created,**kwargs):
    if created:
        group= Group.objects.get(name='Customers')
        user = instance.user
        user.groups.add(group)
      
@receiver(post_save,sender=Customer)
def save_customer(sender,instance,**kwargs):
    instance.save

@receiver(post_save,sender=Trader)
def add_to_traders_group(sender,instance,created,**kwargs):
    if created:
        group= Group.objects.get(name='Traders')
        user = instance.user
        user.groups.add(group)
      
@receiver(post_save,sender=Trader)
def save_trader(sender,instance,**kwargs):
    instance.save
