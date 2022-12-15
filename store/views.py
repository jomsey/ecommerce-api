from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import permissions,mixins,status,exceptions
from main.models import CustomUser
from .models import (Cart, FeaturedProduct, 
                         Product, ProductInstance, Trader,
                         ProductReview,ProductCategory,
                         Promotion,
                         Order,Customer,CustomerWishList,ProductsCollection)
from . import permissions as base_p
from . import filters
from  store.serializers import (AdminAccessUserSerializer, CartSerializer, DisplayFeaturedProductSerializer,
                              EditUserSerializer, FeaturedProductSerializer,
                              ProductInstanceSerializer, PromotionSerializer,
                              ProductCategorySerializer, ProductReviewSerializer,
                              ProductSerializer,DetailedProductInstanceSerializer,
                               OrderSerializer,CustomerSerializer,CustomerWishListSerializer, 
                               UpdateOrderSerializer, UserSerializer,TraderSerializer,ProductsCollectionSerializer,
                               
    )


class CustomUserViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,GenericViewSet):
    """
    Only accessed by authenticated users.
    Customers or traders have access to  only their user profiles.
    Superuser can access all user profiles.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request:
            user = self.request.user
            return CustomUser.objects.prefetch_related('groups').all() if user.is_staff else  CustomUser.objects.prefetch_related('groups').filter(id=user.id)

    def get_serializer_class(self):
        if self.request:
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                if self.request.user.is_staff:
                    return AdminAccessUserSerializer
                return EditUserSerializer 
        return UserSerializer
    
    
class ProductViewSet(ModelViewSet):
    """
    ReadOnly for customers and anonymous users
    """
    serializer_class = ProductSerializer
    filterset_class = filters.ProductFilter
    search_fields = ['name', 'category__name',]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        
        context = super().get_serializer_context()
        
        if self.request:
            context['user']=self.request.user
            
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
        return Product.objects.select_related('promotion','category','trader').all()
            
           
class ProductReviewViewSet(ModelViewSet):
    """
    Customer reviews on products.
    Only logged in users can make reviews.
    Cannot delete or edit someone's reviews
    ReadOnly to anonymous users
    """

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
        if self.request.user.id != instance.customer.id:
            raise exceptions.PermissionDenied('Not Authorized to delete other person\'s review')
        super().perform_destroy(self, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if self.request.user.id != instance.customer.id:
                raise exceptions.PermissionDenied('Not Authorized to edit other person\'s review')
            
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.product_set.count() > 0:
            return Response({'detail':'Cannot delete some instances of ProductCategory because they are referenced through protected foreign keys'},status=status.HTTP_405_METHOD_NOT_ALLOWED)    
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class PromotionViewSet(ModelViewSet):
    """
       ReadOnly to customers and anonymous users
    """
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
class FeaturedProductViewSet(ModelViewSet):
    """
       ReadOnly to customers and anonymous users
    """
    queryset = FeaturedProduct.objects.select_related('product').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.request:
            if self.request.method == 'GET':
                return DisplayFeaturedProductSerializer
        return  FeaturedProductSerializer

         
class ProductInstanceViewSet(ModelViewSet):
    """
    Product to be added to the cart or wishlist
    """
    
    def get_serializer_class(self):
        if self.request:
            if self.request.method=='GET':
                return DetailedProductInstanceSerializer
        return ProductInstanceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_pk'] = self.kwargs.get('cart_pk')
        return context

    def get_queryset(self):
        wish_list_pk = self.kwargs.get('wish_list_pk')

        if wish_list_pk:
            #use this queryset to get product instances from  a particular wishlist
            return  ProductInstance.objects.filter(wish_list_id=wish_list_pk).all()
       
        #getting products from a particular cart
        cart_pk=self.kwargs.get('cart_pk')
        return ProductInstance.objects.select_related("product").filter(cart_id=cart_pk)

     
class CartViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,
                GenericViewSet):
    """
    Anonymous users can create a shopping cart
    """
    serializer_class = CartSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        return Cart.objects.all()
    
    
class OrderViewSet(ModelViewSet):
    """
    Order created by user.
    For user to create an order,should be authenticated.
    Order consists a cart with product instances.
    A user a can create more than one orders.
    User cannot make an order with an empty cart
    User can only access to their orders unless they are super users
    """

    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request:
            if self.request.method == 'PUT':
                return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
       if self.request:
            user = self.request.user
            if user.is_staff:
                return Order.objects.select_related('cart','customer').all()
            return Order.objects.select_related('cart','customer').filter(customer_id=user.id)

    
class CustomerViewSet(mixins.CreateModelMixin,GenericViewSet):
    serializer_class =CustomerSerializer
    
    def get_queryset(self):
        if self.request:
            user = self.request.user
            if  user.is_staff:
                return Customer.objects.all()
            return Customer.objects.filter(user=user.id)

class TraderViewSet(mixins.CreateModelMixin,GenericViewSet):
    serializer_class =TraderSerializer
    
    def get_queryset(self):
        if self.request:
            user = self.request.user
            if  user.is_staff:
                return Trader.objects.all()
            return Trader.objects.filter(user=user.id)
          

class CustomerWishListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    """
    Create endpoint not provided because customer wishlist is created while creating a customer.
    Only authenticated users can create a wishList.
    Customers should only access their wishlists.
    """
    queryset = CustomerWishList.objects.all()
    serializer_class =CustomerWishListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['wish_list_pk'] = self.kwargs.get('wish_list_pk')
        return context

    def get_queryset(self):
       if self.request:
            return CustomerWishList.objects.filter(customer_id=self.request.user.id)

class ProductsCollectionViewSet(ModelViewSet):
    queryset = ProductsCollection.objects.prefetch_related("products")
    serializer_class = ProductsCollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
