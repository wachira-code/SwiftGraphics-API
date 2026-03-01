from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .models import Service, Order, BusinessCardDesign, EulogyDocument
from .serializers import (
	ServiceSerializer, OrderSerializer,
	BusinessCardDesignSerializer, EulogyDocumentSerializer,
	RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer
)

User = get_user_model()

class StandardPagination(PageNumberPagination):
	page_sie = 10
	page_size_query_param = 'page_size'
	max_page_size = 100
	
class IsAdminOrReadOnly(permissions.BasePermission):
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
				'user': {'id': user.id, 'username': user.username, 'email': user.email}
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
		
class ChangePasswordView(generics.GenericAPIView):
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
	serializer_class = ServiceSerializer
	permission_classes = [IsAdminOrReadOnly]
	pagination_class = StandardPagination
	filter_backends = [filters.SearchFilter]
	search_fields = ['name', 'service_type', 'description']
	
	def get_queryset(self):
		queryset = Service.objects.all()
		service_type = self.request.query_params.get('service_type')
		if service_type:
			queryset = queryset.filter(service_type=service_type)
		return queryset.order_by('-created_at')
		
class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
	permission_classes = [IsAdminOrReadOnly]
	
	def destroy(self, request, *args, **kwargs):
		service = self.get_object()
		service_name = service.name
		service.delete()
		return Response({'message': f'Service "{service_name}" deleted successfully'}, status=status.HTTP_200_OK)
		
class OrderListCreateView(generics.ListCreateAPIView):
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = StandardPagination
	filter_backends = [filters.SearchFilter]
	search_fields = ['status', 'service__name']

	def get_queryset(self):
        	queryset = Order.objects.filter(
            		customer=self.request.user
        	)
        	status_filter = self.request.query_params.get('status')
        	if status_filter:
            		queryset = queryset.filter(status=status_filter)
        	return queryset.order_by('-created_at')

	def perform_create(self, serializer):
        	serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Order.objects.filter(customer=self.request.user)

	def destroy(self, request, *args, **kwargs):
		order = self.get_object()
		if order.status not in ['pending']:
			return Response(
				{'error': 'Only pending orders can be cancelled.'},
				status=status.HTTP_400_BAD_REQUEST
			)
		order.status = 'cancelled'
		order.save()
		return Response(
			{'message': f'Order #{order.id} cancelled successfully.'},
			status=status.HTTP_200_OK
		)

class OrderStatusUpdateView(generics.UpdateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAdminUser]

	def patch(self, request, *args, **kwargs):
		order = self.get_object()
		new_status = request.data.get('status')
		valid_statuses = ['pending', 'processing', 'completed', 'cancelled']

		if new_status not in valid_statuses:
			return Response(
				{'error': f'Invalid status. Choose from {valid_statuses}'},
				status=status.HTTP_400_BAD_REQUEST
			)

		order.status = new_status
		order.save()
		return Response(
			{
				'message': f'Order #{order.id} status updated to {new_status}.',
				'order': OrderSerializer(order).data
			},
			status=status.HTTP_200_OK
		)


class BusinessCardListCreateView(generics.ListCreateAPIView):
	serializer_class = BusinessCardDesignSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = StandardPagination

	def get_queryset(self):
		return BusinessCardDesign.objects.filter(
			order__customer=self.request.user
		).order_by('-id')

	def perform_create(self, serializer):
		order = get_object_or_404(
			Order,
			pk=self.kwargs['order_id'],
			customer=self.request.user
		)
		serializer.save(order=order)

class BusinessCardDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = BusinessCardDesignSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return BusinessCardDesign.objects.filter(
			order__customer=self.request.user
		)

	def destroy(self, request, *args, **kwargs):
		design = self.get_object()
		design.delete()
		return Response(
			{'message': 'Business card design deleted successfully.'},
			status=status.HTTP_200_OK
		)

class EulogyListCreateView(generics.ListCreateAPIView):
	serializer_class = EulogyDocumentSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = StandardPagination

	def get_queryset(self):
		return EulogyDocument.objects.filter(
			order__customer=self.request.user
		).order_by('-id')

	def perform_create(self, serializer):
		order = get_object_or_404(
			Order,
			pk=self.kwargs['order_id'],
			customer=self.request.user
		)
		serializer.save(order=order)

class EulogyDetailView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = EulogyDocumentSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	def get_queryset(self):
		return EulogyDocument.objects.filter(
			order__customer=self.request.user
		)

	def destroy(self, request, *args, **kwargs):
		eulogy = self.get_object()
		eulogy.delete()
		return Response(
			{'message': 'Eulogy document deleted successfully.'},
			status=status.HTTP_200_OK
		)

class DashboardView(APIView):
	permission_classes = [permissions.IsAdminUser]

	def get(self, request):
		from django.db.models import Sum
		data = {
			'total_orders': Order.objects.count(),
			'pending_orders': Order.objects.filter(status='pending').count(),
			'processing_orders': Order.objects.filter(status='processing').count(),
			'completed_orders': Order.objects.filter(status='completed').count(),
			'cancelled_orders': Order.objects.filter(status='cancelled').count(),
			'total_services': Service.objects.count(),
			'total_customers': User.objects.count(),
			'total_revenue': Order.objects.filter(
				status='completed'
			).aggregate(Sum('total_price'))['total_price__sum'] or 0,
			'business_cards_ordered': BusinessCardDesign.objects.count(),
			'eulogies_ordered': EulogyDocument.objects.count(),
		}
		return Response(data, status=status.HTTP_200_OK)
