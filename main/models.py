from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from uuid import uuid4


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email address',unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=150 ,blank=True)
    
    class Meta(AbstractUser.Meta):
           swappable = 'AUTH_USER_MODEL'

class Cart(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    cart_uuid = models.UUIDField(primary_key=True,default=uuid4)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class CustomerWishList(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.customer.user.username}-WishList'

    
class FeaturedProduct(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    
    def __str__(self) :
        return str(self.product)
    
      
class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='product_name')
    price =models.PositiveIntegerField()
    description = models.TextField(max_length=1000,verbose_name='product_description')
    image_url = models.URLField(max_length=3000)
    category  = models.ForeignKey('ProductCategory', on_delete=models.PROTECT,blank=True,null=True)
    discount = models.PositiveIntegerField(default=0)
    product_uuid = models.UUIDField(editable=False,default=uuid4) # #unique product id
    promotion =models.ForeignKey('Promotion',on_delete=models.SET_NULL,null=True,blank=True)
    trader = models.ForeignKey('Trader',on_delete=models.CASCADE,related_name='trader_products')
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ProductInstance(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)#product bought by customer
    product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4) # #unique product id
    product_count = models.PositiveIntegerField(verbose_name='number of product',default=1)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,related_name='cart_products')
    wish_list =  models.ForeignKey(CustomerWishList,on_delete=models.CASCADE,blank=True,null=True,related_name='products')
    
    def __str__(self):
        return str(self.product)
    
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'ProductCategories'
    
    
class ProductSpecification(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    weight  = models.PositiveIntegerField()
    main_material = models.CharField(max_length=200,blank=True)
    model =models.CharField(max_length=200,blank=True) 


class ProductReview(models.Model):
    
    PRODUCT_VERY_POOR_RATING = 1
    PRODUCT_POOR_RATING = 2
    PRODUCT_GOOD_RATING =3
    PRODUCT_VERY_GOOD_RATING = 4
    PRODUCT_EXCELLENT_RATING = 4
    
    RATE_CHOICES = [
        (PRODUCT_VERY_POOR_RATING,PRODUCT_VERY_POOR_RATING),
        (PRODUCT_POOR_RATING,PRODUCT_POOR_RATING),
        (PRODUCT_GOOD_RATING,PRODUCT_VERY_GOOD_RATING),
        (PRODUCT_VERY_GOOD_RATING,PRODUCT_VERY_GOOD_RATING),
        (PRODUCT_EXCELLENT_RATING,PRODUCT_EXCELLENT_RATING)
    ]
    customer=models.ForeignKey('Customer',on_delete= models.CASCADE) #customer making product review
    product = models.ForeignKey(Product,on_delete=models.CASCADE) #product being reviewed
    date_made = models.DateField(auto_now_add=True)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(verbose_name='product_rating',choices=RATE_CHOICES,default=RATE_CHOICES[2][1])
    
    def __str__(self) :  
        #return the first 30 characters of the product name
        if len(self.product.name) > 30:
            return f'{self.product.name[:30]}..review'
        else:
            return self.product.name
        
         
class Order(models.Model):
    STATUS = [
        ('P','Pending'),
        ('D','Delivered')
    ]
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_made = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE)#contains products ordered
    order_id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    status = models.CharField(max_length=1,choices=STATUS,default="P")
    is_canceled = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.order_id)
    
    
class Promotion(models.Model):
    name = models.CharField(max_length=150)
    description=models.TextField(null=True)
    starting_date=models.DateTimeField(auto_created=True)#will change on deploy
    ending_on = models.DateTimeField(auto_created=True)
    trader = models.ForeignKey('Trader',on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.name


class Trader(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    

