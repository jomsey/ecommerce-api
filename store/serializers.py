from rest_framework import serializers,exceptions
from drf_writable_nested.serializers import WritableNestedModelSerializer
from . models import (Cart, FeaturedProduct, Trader,
                      Product, ProductCategory, ProductInstance,
                      ProductReview,ProductSpecification,
                      Promotion,Order,Customer,CustomerWishList)
from main.models import CustomUser


class AdminAccessUserSerializer(serializers.ModelSerializer):
     class Meta:
            model = CustomUser
            fields = ['is_active','is_staff']
            
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','password','email','phone_number','address','is_active']
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(source='password',write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id','username','password','password2','email','phone_number','address']
      
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField('get_discounted_price')
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
    
    
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','name',]
        

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['product_id','main_material','weight','model']

    def create(self,validated_data):
        product_pk =self.context.get('product_pk')
        return ProductSpecification.objects.create(product_id=product_pk,**validated_data)


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
        
        
class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ['product','product_uuid','product_count',]
       
    def create(self,validated_data):
        cart_pk =self.context.get('cart_pk')
        wish_list_pk = self.context.get('wish_list_pk')

        if wish_list_pk:
            #adding product to wishlist
            return ProductInstance.objects.create(wishlist_id=wish_list_pk,**validated_data)
        #adding product to a cart
        return ProductInstance.objects.create(cart_id=cart_pk,**validated_data)

        
class CartSerializer(serializers.ModelSerializer):
    cart_uuid = serializers.UUIDField(read_only = True)
    class Meta:
        model = Cart
        fields =['cart_uuid','date_created']


    def create(self,validated_data):
        request = self.context.get('request')
        cart = Cart.objects.create()

        #create a cart uuid session
        request.session['cart_uuid'] = str(cart.cart_uuid)
        request.session.modified = True
        return cart


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =['status']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Order
        fields =['customer','cart','order_id','status','date_made']


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

    
class CustomerWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWishList
        fields =['id','customer_id','products']

class TraderSerializer(WritableNestedModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Trader
        fields = ['id','user',]
