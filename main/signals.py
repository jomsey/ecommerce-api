from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from main.models import Customer,CustomerWishList,Trader,Order,Payment


@receiver(post_save,sender=Customer)
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
    
# @receiver(post_save,sender=Order)    
# def create_order_payment(sender,instance,created,**kwargs):
#         if created:
#                 Payment.objects.create(order=instance)
                
# @receiver(post_save,sender=Order) 
# def save_create_order_payment(sender,instance,**kwargs):
#         instance.save()