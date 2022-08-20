from django_filters.rest_framework import FilterSet
from main.models import Product

class ProductFilter(FilterSet):
	class Meta:
		model = Product
		fields = {
            'price': ['lte', 'gte'],
        }

