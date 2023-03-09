from main.models import CustomUser
from rest_framework import serializers,exceptions
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth.password_validation import validate_password
from . models import (Cart, FeaturedProduct, Trader,
                      Product, ProductCategory, ProductInstance,
                      ProductReview,WishListProductInstance,
                      Promotion,Order,Customer,CustomerWishList,ProductsCollection)


class AdminAccessUserSerializer(serializers.ModelSerializer):
     class Meta:
            model = CustomUser
            fields = ['is_active','is_staff']
            
            
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','email','phone_number','address','is_active']
    
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only = True)
    customerwishlist = serializers.PrimaryKeyRelatedField(read_only=True)

    

    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','password','password2','email','phone_number','address','customerwishlist']
      
    def validate(self, data):
        if data["password"] == data["password2"]:
            validate_password(data["password"])
            return super().validate(data)
        raise serializers.ValidationError({"error":"Both password fields must be matching"})

    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data["username"],
                                              email=validated_data["email"],
                                              password=validated_data["password"])
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','name',]

class ProductCollectionSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField('get_discounted_price')

    class Meta:
        model = Product
        fields = ['id','name','price','description','image_url','discount','discounted_price']

    def get_discounted_price(self,product:Product):
        discount = (product.discount/100)*product.price
        return product.price - discount


class SimpleCartProductInstanceSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField('get_discounted_price')
  
    class Meta:
        model = Product
        fields = ['id','name','price','image_url','discount','discounted_price']

    def get_discounted_price(self,product:Product):
        discount = (product.discount/100)*product.price
        return product.price - discount

        
        
class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField('get_discounted_price')
    category = ProductCategorySerializer()
    class Meta:
        model = Product
        fields = ['id','name','price','description','image_url','discount','discounted_price','promotion','category']
        
    def get_discounted_price(self,product:Product):
        discount = (product.discount/100)*product.price
        return product.price - discount
    
    def create(self, validated_data):
        category_pk = self.context.get('category_pk')
        promotion_pk = self.context.get('promotion_pk')
        user = self.context.get('user')
        trader = Trader.objects.get(user=user)

        if category_pk:
            #add a  product  with a category field
            return  Product.objects.create(category_id=category_pk,**validated_data)

        if promotion_pk:
            #create a product with a promotion field
            return Product.objects.create(promotion_id=promotion_pk,**validated_data)
        return Product.objects.create(trader=trader,**validated_data)


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =ProductReview
        fields = ['id','customer_id','review','date_made','rating']
    
    def create(self, validated_data):
        product_pk = self.context['product_pk']
        user = self.context['request'].user #current logged user       
        return ProductReview.objects.create(product_id = product_pk,customer_id=user.id, **validated_data)
    
    
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id','name','description','starting_date','ending_on']
      
        
class DisplayFeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = FeaturedProduct
        fields =[ 'product',]
        
        
class FeaturedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedProduct
        fields =[ 'product',]

        
class DetailedProductInstanceSerializer(serializers.ModelSerializer):
    product = SimpleCartProductInstanceSerializer()
    class Meta:
        model = ProductInstance
        fields = ['product','product_uuid','product_count',]

      
class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ['product','product_uuid','product_count',]
       
    def create(self,validated_data):
        cart_pk =self.context.get('cart_pk')
        return ProductInstance.objects.create(cart_id=cart_pk,**validated_data)


class DetailedCartSerializer(serializers.ModelSerializer):
    cart_uuid = serializers.UUIDField(read_only = True)
    cart_products = DetailedProductInstanceSerializer(many=True)
    class Meta:
        model = Cart
        fields =['cart_uuid','date_created',"cart_products"]  
        
          
class CartSerializer(serializers.ModelSerializer):
    cart_uuid = serializers.UUIDField(read_only = True)
    
    class Meta:
        model = Cart
        fields =['cart_uuid','date_created']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =['status']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.ReadOnlyField()
    payment_status = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields =['customer','cart','order_id','status','date_made','payment_status']

    def create(self, validated_data):
        user = self.context['request'].user #current logged user   
        cart = validated_data.get('cart')
        
        if cart:
            if cart.cart_products.count() == 0:
                raise exceptions.ValidationError({'detail':'Can not create an order with an empty cart'})

            return Order.objects.create(customer_id = user.id, **validated_data)
        raise exceptions.ValidationError({'detail':'Can not create an order without a cart'})
      

class CustomerSerializer(WritableNestedModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Customer
        fields = ['id','user',]


class TraderSerializer(WritableNestedModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Trader
        fields = ['id','user',]


class ProductsCollectionSerializer(serializers.ModelSerializer):
    products = ProductCollectionSerializer(many=True)
    class Meta:
        model =  ProductsCollection
        fields = ['id','title','products']


class CustomerWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWishList
        fields =['id','customer_id']


class SimpleWishListProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = ['id','name','price','image_url',]


class WishListProductInstanceSerializer(serializers.ModelSerializer):
    product = SimpleWishListProductSerializer()
    class Meta:
        model = WishListProductInstance
        fields = ["product","wish_list","product_uuid"]


class SimpleWishListProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListProductInstance
        fields = ["product","wish_list","product_uuid"]
