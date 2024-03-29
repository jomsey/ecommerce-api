from django.db import models
from django.conf import settings
from uuid import uuid4
from datetime import date

class Cart(models.Model):
    date_created = models.DateField(auto_now_add=True)
    cart_uuid = models.UUIDField(primary_key=True,default=uuid4)
    
    @property
    def can_be_deleted(self):
        NUMBER_OF_DAYS_TILL_DELETE = 30
        cart_age = (date.today() - self.date_created).days
        return cart_age>NUMBER_OF_DAYS_TILL_DELETE


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CustomerWishList(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.customer.username}-WishList'

    
class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='product name',help_text='This is the name of the product')
    price =models.PositiveIntegerField(help_text='Any positive integer number')
    description = models.TextField(verbose_name='product description',max_length=10000)
    image_url = models.URLField(verbose_name='image url',max_length=3000,help_text='product image address')
    category  = models.ForeignKey('ProductCategory', on_delete=models.PROTECT,blank=True,null=True)
    subcategory = models.ForeignKey('Subcategory',on_delete=models.PROTECT,blank=True,null=True)
    discount = models.PositiveIntegerField(default=0)
    product_uuid = models.UUIDField(verbose_name='product uuid',editable=False,default=uuid4,help_text='unique product identification number') # #unique product id
    promotion =models.ForeignKey('Promotion',on_delete=models.SET_NULL,null=True,blank=True)
    trader = models.ForeignKey('Trader',on_delete=models.CASCADE,related_name='trader_products',help_text='product merchant')
    date_added = models.DateField(verbose_name='date added to store',auto_now_add=True)

    def __str__(self):
        return self.name


class ProductInstance(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)#product bought by customer
    product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4) # #unique product id
    product_count = models.PositiveIntegerField(verbose_name='number of product',default=1)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_products')
    
    def __str__(self):
        return str(self.product)

    class Meta:
        ordering = ["product"]
 
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'ProductCategories'

class Subcategory(models.Model):
    name = models.CharField(max_length=200,help_text='product sub category')
    category =  models.ForeignKey('ProductCategory',on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Sub-categories'

# class ProductImage(models.Model):
#     image = models.ImageField(upload_to='products/images')
  
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
    PRODUCT_EXCELLENT_RATING = 5
    
    RATE_CHOICES = [
        (PRODUCT_VERY_POOR_RATING,PRODUCT_VERY_POOR_RATING),
        (PRODUCT_POOR_RATING,PRODUCT_POOR_RATING),
        (PRODUCT_GOOD_RATING,PRODUCT_VERY_GOOD_RATING),
        (PRODUCT_VERY_GOOD_RATING,PRODUCT_VERY_GOOD_RATING),
        (PRODUCT_EXCELLENT_RATING,PRODUCT_EXCELLENT_RATING)
    ]
    
    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete= models.CASCADE) #customer making product review
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
  
class FeaturedProduct(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    
    def __str__(self) :
        return str(self.product)

         
class Order(models.Model):
    DELIVERY_STATUS = [
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('Canceled','Canceled')
    ]
    
    PAYMENT_STATUS = [
        ('Pending','Pending'),
        ('Complete','Complete')    
    ]
    
    payment_status = models.CharField(max_length=10,choices=PAYMENT_STATUS,default="Pending")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_made = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart,on_delete=models.SET_NULL,null=True)#contains products ordered
    order_id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    status = models.CharField(max_length=10,choices=DELIVERY_STATUS,default="Pending")
  
    def __str__(self):
        return f'{self.customer}_order'
    
    
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


class ProductsCollection(models.Model):
    title = models.CharField(max_length=50)
    products =models.ManyToManyField(Product)

    def __str__(self):
        return self.title

class WishListProductInstance(models.Model):
    product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4) # #unique product id
    product = models.ForeignKey(Product,on_delete=models.CASCADE)#product bought by customer
    wish_list =  models.ForeignKey(CustomerWishList,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name