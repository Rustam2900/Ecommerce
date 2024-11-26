from .models import Contact
from rest_framework import serializers


class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('first_name', 'email', 'phone', 'message')
