from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .models import Service, Order, BusinessCardDesign, EulogyDocument
from .serializers import (
    ServiceSerializer, OrderSerializer,
    BusinessCardDesignSerializer, EulogyDocumentSerializer,
    RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer
)

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    """Only admins can create/edit services."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]
	
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			token = Token.objects.get(user=user)
			return Response({
				'token': token.key,
				'user': {'id': user.id, 'username': user.username 'email': user.email}
			},
				status=status.HTTP_201_CREATED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
		
class LoginView(generics.GenericAPIView):
	serializer_class = LoginSerializer
	permission_classes = [permissions.AllowAny]
	
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = authenticate(
				username=serializer.validated_data['username'],
				password=serializer.validated_data['password']
			)
			if user:
				token, _ = Token.objects.get_or_create(user=user)
				return Response({
					'token': token.key,
					'user': {'id': user.id, 'username': user.username, 'email': user.email}
				}, status=status.HTTP_200_OK)
			return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
		return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
		
class LogoutView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request):
		request.user.auth_token.delete()
		return Response({'message': 'Logged out successfullly'}, status=status.HTTP_200_OK)
		
class UserProfileView(generics.GenericAPIView):
	serializer_class = UserProfileSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request):
		serializer = self.get_serializer(request.user)
		return Response(serializer.data)
		
	def put(self, request):
		serializer = self.get_serializer(request.user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class ChangePasswordViw(generics.GenericAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = request.user
			if not user.check_password(serializer.validated_data['old_password']):
				return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
			user.set_password(serializer.validated_data['new_password'])
			user.save()
			Token.objects.filter(user=user).delete()
			new_token = Toke.objects.create(user=user)
			return Response({'message': 'Password changed successfully', 'token': new_token.key}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_available=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

