from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import permissions,mixins,status
from django.shortcuts import get_object_or_404
from main.models import (Cart, FeaturedProduct, 
                         Product, ProductInstance, 
                         ProductReview,ProductCategory,
                         ProductSpecification,Promotion,
                         Order,Customer,CustomerWishList)
from main import permissions as base_p
from main.serializers import (CartSerializer, FeaturedProductSerializer,
                              ProductInstanceSerializer, PromotionSerializer,
                              ProductCategorySerializer, ProductReviewSerializer,
                              ProductSerializer,ProductSpecificationSerializer,
                               OrderSerializer,CustomerSerializer,CustomerWishListSerializer
    )

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['category_pk'] = self.kwargs.get('category_pk')
        context['promotion_pk'] = self.kwargs.get('promotion_pk')
        return context
    
    def get_queryset(self):
        category_pk = self.kwargs.get('category_pk')
        promotion_pk = self.kwargs.get('promotion_pk')

        if category_pk:
            #use this queryset to get products from  a particular category
            return  Product.objects.filter(category_id=category_pk).select_related('category')

        if promotion_pk:
            #use this queryset to get products in a particular promotion
            return Product.objects.filter(promotion_id=promotion_pk).select_related('promotion')
        return Product.objects.all()
            
           
class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context
    
    
class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.product_set.count() > 0:
            return Response({'error':'Cannot delete some instances of ProductCategory because they are referenced through protected foreign keys'},status=status.HTTP_405_METHOD_NOT_ALLOWED)    
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductSpecificationViewSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 GenericViewSet):
    
    """Product specification objects should not be listed or deleted
       Only registered and authorised users can add,edit or delete a product specification
    """

    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        """
        adding product_pk to the context to be used in retriving  a product's specification
        """
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
class FeaturedProductViewSet(ModelViewSet):
    queryset = FeaturedProduct.objects.select_related('product').all()
    serializer_class = FeaturedProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
class ProductInstanceViewSet(ModelViewSet):
    """
    AnonymousUser is able to add product to the shopping cart 
    """
    serializer_class = ProductInstanceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_pk'] = self.kwargs.get('cart_pk')
        return context

    def get_queryset(self):
        """
        getting products from a paticular cart
        """
        cart_pk=self.kwargs.get('cart_pk')
        return ProductInstance.objects.filter(cart_id=cart_pk).all()

  
    
class CartViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                GenericViewSet):
    """
    Anonymous users should be able to create a shopping cart
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    
class OrderViewSet(ModelViewSet):
    """
    Order created by user.
    For user to create an order,should be authenticated.
    Order consists a cart with product instances.
    A user a can create more than one orders.
    User cannot make an order with an empty cart
    """
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def get_cart_items_count(self):
    #     order = Order.objects.last()
    #     if order.cart:
    #         cart_items_count = order.cart.productinstance_set.all()
    #         print(cart_items_count)

    #         if cart_items_count:
    #             self.kwargs['cart_items_count'] =  cart_items_count
    #             return
    #     return Response({'Error':'Cannot create an order with an empty cart'})




    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['customer_pk'] = self.kwargs.get('customer_pk')
        return context

    def get_queryset(self):
        return Order.objects.select_related('cart','customer').filter(customer_id=self.kwargs.get('customer_pk'))

    
    
class CustomerViewSet(
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class =CustomerSerializer


class CustomerWishListViewSet(
                      mixins.RetrieveModelMixin,
                     GenericViewSet):
    """
    create endpoint not provided because customer wishlist is created while creating a customer
    """
    queryset = CustomerWishList.objects.all()
    serializer_class =CustomerWishListSerializer

    # def get_queryset(self):
    #     return CustomerWishList.objects.get(customer_id=self.kwargs['customer_pk'])






