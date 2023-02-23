from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from .serializers import ProductSerializer

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": 19.99
        }
        self.response = self.client.post(
            reverse("product-list"), self.product_data, format="json"
        )

    def test_create_product(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(
            Product.objects.get().name, self.product_data["name"]
        )
        self.assertEqual(
            Product.objects.get().description, self.product_data["description"]
        )
        self.assertEqual(
            Product.objects.get().price, self.product_data["price"]
        )

    def test_get_product_list(self):
        response = self.client.get(reverse("product-list"))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        product = Product.objects.get()
        response = self.client.get(reverse("product-detail", args=[product.id]))
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        product = Product.objects.get()
        new_product_data = {
            "name": "Updated Product",
            "description": "This is an updated product",
            "price": 29.99
        }
        response = self.client.put(
            reverse("product-detail", args=[product.id]), new_product_data, format="json"
        )
        updated_product = Product.objects.get()
        serializer = ProductSerializer(updated_product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        product = Product.objects.get()
        response = self.client.delete(reverse("product-detail", args=[product.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)