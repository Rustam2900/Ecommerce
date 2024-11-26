from django.db.models import F
from rest_framework import serializers

from products.serializers import ProductCategorySerializers
from .models import Product, ProductBasket, Basket


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']


class ProductBasketSerializer(serializers.ModelSerializer):
    product = ProductCategorySerializers()

    class Meta:
        model = ProductBasket
        fields = ['id', 'user', 'product', 'quantity', 'sum']


class ProductBasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBasket
        fields = ['id', 'product']

    def create(self, validated_data):
        product_id = validated_data.get('product')
        user = validated_data.get('user')

        # Check if the product already exists in the basket for the given user
        existing_product_basket = ProductBasket.objects.filter(user=user, product_id=product_id).first()
        if existing_product_basket:
            # Product already exists in basket, so increment quantity
            existing_product_basket.quantity += 1
            existing_product_basket.save()
            return existing_product_basket
        else:
            # New product added to basket, quantity set to 1
            validated_data['user'] = user
            validated_data['quantity'] = 1
            return ProductBasket.objects.create(**validated_data)


class ProductBasketPlusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBasket
        fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        product_basket = ProductBasket.objects.get(pk=request.data['id'])
        product_basket.quantity = F('quantity') + 1
        product_basket.save()
        return product_basket


class ProductBasketMinusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBasket
        fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        product_id = request.data['id']
        product_basket = ProductBasket.objects.get(id=product_id)

        if product_basket.quantity == 1:
            product_basket.delete()
        else:
            product_basket.quantity -= 1
            product_basket.save()

        return product_basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        exclude = ['created_at', 'updated_at']
