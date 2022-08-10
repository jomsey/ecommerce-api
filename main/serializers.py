from rest_framework import serializers
from . models import (Cart, FeaturedProduct, 
                      Product, ProductCategory, ProductInstance,
                      ProductReview,ProductSpecification,
                      Promotion,Order,Customer)



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

        if category_pk:
            #add a  product to a category
            return  Product.objects.create(category_id=category_pk,**validated_data)

        if promotion_pk:
            #create a product to a promotion
            return Product.objects.create(promotion_id=promotion_pk,**validated_data)

        return super().create(validated_data)


class ProductReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =ProductReview
        fields = ['customer_id','review','date_made','rating']
    
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
        
        
class FeaturedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = FeaturedProduct
        fields =[ 'product',]
        
        
class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ['product','product_uuid','product_count',]
       
    def create(self,validated_data):
        cart_pk =self.context.get('cart_pk')
        return ProductInstance.objects.create(cart_id=cart_pk,**validated_data)

        
class CartSerializer(serializers.ModelSerializer):
    cart_uuid = serializers.UUIDField(read_only = True)
    class Meta:
        model = Cart
        fields =['cart_uuid',]


class OrderSerializer(serializers.ModelSerializer):
     class Meta:
        model = Order
        fields =['customer','cart','order_id','status']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['profile','phone_number','address']
