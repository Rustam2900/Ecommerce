from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializers


@swagger_auto_schema(request_body=ContactSerializers)
class ContactListAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializers
