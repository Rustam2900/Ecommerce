from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ['created_at', 'updated_at']


class StarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        exclude = ['created_at', 'updated_at']


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ['created_at', 'updated_at']


class SizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ['created_at', 'updated_at']


class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ['created_at', 'updated_at']


class ProductCategorySerializers(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    stars = StarsSerializer()
    discount = DiscountsSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "quantity", "category", "discount", "images", "stars"]


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    color = ColorsSerializer()
    size = SizesSerializer()
    stars = StarsSerializer()
    category = CategorySerializer()
    discount = DiscountsSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "quantity", "description", "category", "color", "size",
                  "images", "stars", "discount"]
