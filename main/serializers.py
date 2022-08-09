from django.shortcuts import get_object_or_404
from rest_framework import serializers
from . models import Product, ProductCategory, ProductReview,ProductSpecification,Promotion



class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField('get_discounted_price')
    class Meta:
        model = Product
        fields = ['id','name','price','description','image_url','discount','discounted_price','category_id']
        
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