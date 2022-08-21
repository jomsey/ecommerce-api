from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from main.models import Customer,CustomerWishList,Trader


@receiver(post_save,sender=Customer)
def create_customer_wish_list(sender,instance,created,**kwargs):
	if created:
            CustomerWishList.objects.create(customer=instance)

@receiver(post_save,sender=Customer)
def save_customer_wish_list(sender,instance,**kwargs):
        instance.save


# @receiver(post_save,sender=Customer)
# def add_to_customers_group(sender,instance,created,**kwargs):
#     if created:
#         group = Group.objects.get_or_create(name='Customers') 
#         print(instance.user.groups)

# @receiver(post_save,sender=Customer)
# def save_customer(sender,instance,**kwargs):
#     instance.save


# @receiver(post_save,sender=Trader)
# def add_to_traders_group(sender,instance,created,**kwargs):
#     if created:
#         Customer.objects.create(user=instance)

# @receiver(post_save,sender=Trader)
# def save_customer(sender,instance,**kwargs):
#     instance.save