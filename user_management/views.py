from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer
from django.db.models import Q


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
    

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User created successfully'
        })
    

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        if search_query:
            user = CustomUser.objects.filter(email__iexact=search_query).first()
            print('user =======>>>>>>>>>>> ',user)
            if user:
                return CustomUser.objects.filter(email__iexact=search_query)
            else:
                return CustomUser.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        return CustomUser.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)