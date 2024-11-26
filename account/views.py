import random

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ChangePasswordSerializer, UpdateUserSerializer, \
    RegisterSerializer, MyTokenObtainPairSerializer, ForgetPasswordSerializer, \
    ForgetChangePasswordSerializers
from drf_yasg.utils import swagger_auto_schema
from .models import User

import smtplib
import ssl


# register

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# change user
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class ForgetPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgetPasswordSerializer)
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

            # Parolni tiklash uchun kod yaratish
            code = ''.join(random.choices('0123456789', k=6))
            user.gmail_code = code
            user.save()

            # Email yuborish
            context = ssl.create_default_context()
            port = 465
            sender_email = 'sardor_shukurov2003S@mail.ru'
            password = 'dgm20y86ReJZXSEpvphz'  # Bu o'zgaruvchini o'zgartiring
            with smtplib.SMTP_SSL("smtp.mail.ru", port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, [email], f'Sizning parolni tiklash uchun kod: {code}')

            return Response({'message': 'Parolni tiklash uchun kod yuborildi'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetChangePasswordView(APIView):
    serializer_class = ForgetChangePasswordSerializers

    @swagger_auto_schema(request_body=ForgetChangePasswordSerializers)
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        User = get_user_model()
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            code = serializer.validated_data.get('code')

            user = User.objects.filter(gmail_code=code, email=email).first()  # Kodni tekshirish

            if user:  # Agar kod to'g'ri bo'lsa
                user.set_password(password)
                user.save()
                return Response({'message': 'Successful password changed'}, status=status.HTTP_200_OK)
            else:  # Agar kod noto'g'ri bo'lsa yoki topilmagan bo'lsa
                return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
