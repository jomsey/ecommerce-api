from django_filters.rest_framework import FilterSet
from main.models import Order, Product

class ProductFilter(FilterSet):
	class Meta:
		model = Product
		fields = {
            'price': ['lte', 'gte'],
        }

class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
			'customer':[]
		}

