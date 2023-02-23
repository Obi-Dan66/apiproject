import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from catalog.models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def new_product():
    return Product.objects.create(name='Test Product', description='Test Description')


def test_create_product(api_client):
    url = reverse('product-list')
    data = {'name': 'Test Product', 'description': 'Test Description'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.get().name == 'Test Product'


def test_get_product(api_client, new_product):
    url = reverse('product-detail', args=[new_product.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Product'
    assert response.data['description'] == 'Test Description'


def test_update_product(api_client, new_product):
    url = reverse('product-detail', args=[new_product.id])
    data = {'name': 'Updated Test Product', 'description': 'Updated Test Description'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Updated Test Product'
    assert response.data['description'] == 'Updated Test Description'


def test_delete_product(api_client, new_product):
    url = reverse('product-detail', args=[new_product.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0