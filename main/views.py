from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import permissions,mixins,status
from main.models import Product, ProductReview,ProductCategory,ProductSpecification,Promotion
from main.serializers import PromotionSerializer, ProductCategorySerializer, ProductReviewSerializer, ProductSerializer,ProductSpecificationSerializer


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
            return  Product.objects.filter(category_id=category_pk)

        if promotion_pk:
            #use this queryset to get products in a particular promotion
            return Product.objects.filter(promotion_id=promotion_pk)
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
                                 GenericViewSet,):
    
    "Product specification objects should not be listed or deleted"
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_pk'] = self.kwargs.get('product_pk')
        return context


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    