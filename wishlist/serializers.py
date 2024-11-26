from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from .models import Wishlist


class WishlistGetSerializer(serializers.ModelSerializer):
    wishlist_pro = ProductSerializer()

    class Meta:
        model = Wishlist
        exclude = ['created_at', 'updated_at']


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ["wishlist_pro"]

    # def __init__(self, *args, **kwargs):
    #     super(WishlistSerializer, self).__init__(*args, **kwargs)
    #
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserSerializers(instance.user).data
    #     response['product'] = ProductSerializers(instance.product).data
    #     return response
