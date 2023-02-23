import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Offer
from .serializers import ProductSerializer, OfferSerializer
from django.conf import settings


@api_view(['POST'])
def auth(request):
    """
    Authenticate with the offers microservice to get an access token.
    """
    response = requests.post(
        f"{settings.OFFERS_MS_BASE_URL}/auth"
    )
    if response.status_code != 201:
        return Response(status=response.status_code)
    return Response(response.json(), status=response.status_code)


@api_view(['POST'])
def register_product(request):
    """
    Register a new product with the offers microservice.
    """
    data = json.loads(request.body)
    product_serializer = ProductSerializer(data=data)
    if product_serializer.is_valid():
        product_serializer.save()
        product_id = product_serializer.data['id']
        response = requests.post(
            f"{settings.OFFERS_MS_BASE_URL}/products/register",
            headers={'Authorization': f"Bearer {settings.OFFERS_MS_ACCESS_TOKEN}"},
            data={'id': product_id, 'name': data['name'], 'description': data['description']}
        )
        if response.status_code == 201:
            return Response(product_serializer.data, status=201)
    return Response(product_serializer.errors, status=400)


@api_view(['GET'])
def list_products(request):
    """
    List all products in the product catalog.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update, or delete a product instance.
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['GET'])
def list_product_offers(request, pk):
    """
    List all offers for a given product.
    """
    product = get_object_or_404(Product, pk=pk)
    offers = Offer.objects.filter(product=product)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)