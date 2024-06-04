from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from .models import CustomUser
from rest_framework.response import Response
# Create your views here.


class UserToken(TokenObtainPairView):

    def post(self,request, *args, **kwargs): 

        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email__iexact=email)
            username = user.username
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        request.data["username"] = username
        request.data["password"] = password


        return super().post(request, *args, **kwargs) 