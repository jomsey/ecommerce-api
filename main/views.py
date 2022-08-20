import uuid
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import permissions,mixins,status,exceptions
from django.shortcuts import get_object_or_404
from main.models import (Cart, FeaturedProduct, 
                         Product, ProductInstance, 
                         ProductReview,ProductCategory,
                         ProductSpecification,Promotion,
                         Order,Customer,CustomerWishList)
from main import permissions as base_p
from main import filters
from main.serializers import (CartSerializer, FeaturedProductSerializer,
                              ProductInstanceSerializer, PromotionSerializer,
                              ProductCategorySerializer, ProductReviewSerializer,
                              ProductSerializer,ProductSpecificationSerializer,
                               OrderSerializer,CustomerSerializer,CustomerWishListSerializer
    )

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = filters.ProductFilter
    search_fields = ['name', 'category__name','promotion__name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          base_p.CustomerReadOnly]
    
    
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
        return Product.objects.select_related('promotion','category').all()
            
           
class ProductReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.id != instance.customer.profile.id:
            raise exceptions.PermissionDenied('Not Authorized to delete other person\'s review')
        super().perform_destroy(self, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if self.request.user.id != instance.customer.profile.id:
                raise exceptions.PermissionDenied('Not Authorized to edit other person\'s review')
            
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,base_p.CustomerReadOnly]
    
    
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
       Only registered and authorized users can add,edit or delete a product specification
    """

    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,base_p.CustomerReadOnly]

    def get_serializer_context(self):
        """
        adding product_pk to the context to be used in retrieving  a product's specification
        """
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,base_p.CustomerReadOnly]
    
    
class FeaturedProductViewSet(ModelViewSet):
    queryset = FeaturedProduct.objects.select_related('product').all()
    serializer_class = FeaturedProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    
    
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
        wish_list_pk = self.kwargs.get('wish_list_pk')

        if wish_list_pk:
            #use this queryset to get product instances from  a particular wishlist
            return  ProductInstance.objects.filter(wish_list_id=wish_list_pk).all()
        """
        getting products from a particular cart
        """
        cart_pk=self.kwargs.get('cart_pk')
        return ProductInstance.objects.filter(cart_id=cart_pk).all()

  
    
class CartViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                GenericViewSet):
    """
    Anonymous users should be able to create a shopping cart
    """
    serializer_class = CartSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def get_queryset(self):
        # cart_uuid = self.request.session.get('cart_uuid')
        # x=uuid.UUID(cart_uuid)
        return Cart.objects.all()

    
class OrderViewSet(ModelViewSet):
    """
    Order created by user.
    For user to create an order,should be authenticated.
    Order consists a cart with product instances.
    A user a can create more than one orders.
    User cannot make an order with an empty cart
    """
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.select_related('cart','customer').all()
        return Order.objects.select_related('cart','customer').filter(customer_id=user.id)

    
class CustomerViewSet(
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                     GenericViewSet):
  
    serializer_class =CustomerSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(profile=user.id)
          
        


class CustomerWishListViewSet(
                      mixins.RetrieveModelMixin,
                     GenericViewSet):
    """
    create endpoint not provided because customer wishlist is created while creating a customer
    """
    queryset = CustomerWishList.objects.all()
    serializer_class =CustomerWishListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['wish_list_pk'] = self.kwargs.get('wish_list_pk')
        return context

    def get_queryset(self):
        return CustomerWishList.objects.filter(customer_id=self.request.user.id)


    
