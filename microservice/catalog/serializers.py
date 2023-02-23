from rest_framework import serializers
from .models import Product, Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'price', 'items_in_stock']


class ProductSerializer(serializers.ModelSerializer):
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'offers']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']


class OfferRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
