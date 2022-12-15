from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from main.models import CustomUser
import pytest

class TestCreateProduct:
    def  test_if_user_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/api/products/',{})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_authenticated_but_not_authorized_return_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/api/products/',{})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_authenticated_but_invalid_data_returns_404(self):
        pass
        
    def test_successful_product_creation_returns_201(self):
        pass
           
class TestDeleteProduct:
    def test_if_user_authenticated_but_not_authorized_return_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.delete('/api/products/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def  test_if_user_anonymous_returns_401(self):
        client = APIClient()
        response = client.delete('/api/products/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_authenticated_but_not_authorized_return_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.delete('/api/products/1/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    @pytest.mark.django_db(True)
    def test_if_user_authenticated_but_invalid_data_returns_400(self):
        user = CustomUser.objects.create()
        user.is_staff=True
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/products/',{})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_successful_product_delete_returns_204(self):
        pass
    
class TestProductUpdate:
    pass


class TestCreateProductReview:
    pass

class TesDeleteProductReview:
    pass
    