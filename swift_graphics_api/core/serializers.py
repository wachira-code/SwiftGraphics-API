from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Service, Order, BusinessCardDesign, EulogyDocument

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)
	confirm_password = serializers.CharField(write_only=True)
	
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password', 'confirm_password']
	
	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError("Passwords do not match")
		return data
		
	def create(self, validated_data):
		validated_data.pop('confirm_password')
		user = get_user_model().objects.create_user(
			username=validated_data['username'],
			email=validated_data.get('email', ''),
			password=validated_data['password']
		)
		Token.objects.create(user=user)
		return user
		
class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField(write_only=True)
	
class UserProfileSerializer(serializers.ModelSerializer):
	total_orders = serializers/SerializerMethodField()
	
	class Meta:
		model = User
		fields = ['id', 'usernamr', 'email', 'first_name', 'last_name', 'date_joined', 'total_orders']
		read_only_fields = ['date_joined']
		
	def get_total_orders(self, obj):
		eturn obj.orders.count()
		
class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(write_only=True)
	new_password = serializers.CharField(write_only=True, min_length=8)
	confirm_new_password = serializers.Charfield(write_only=True)
	
	def validate(self, data):
		if data['new_password'] != data['confirm_new_password']:
			raise serializers.ValidationError("New passwords do not match")
		return data

class ServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Service
		fields = '__all__'


class BusinessCardDesignSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusinessCardDesign
		fields = '__all__'
		read_only_fields = ['order']


class EulogyDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = EulogyDocument
		fields = '__all__'
		read_only_fields = ['order']


class OrderSerializer(serializers.ModelSerializer):
	customer = serializers.StringRelatedField(read_only=True)
	service_name = serializers.CharField(source='service.name', read_only=True)
	service_type = serializers.CharField(source='service.service_type', read_only=True)
	business_card_design = BusinessCardDesignSerializer(read_only=True)
	eulogy_document = EulogyDocumentSerializer(read_only=True)

	class Meta:
		model = Order
		fields = [
			'id', 'customer', 'service', 'service_name', 'service_type',
			'quantity', 'special_instructions', 'status', 'total_price',
			'created_at', 'updated_at', 'business_card_design', 'eulogy_document'
		]
		read_only_fields = ['customer', 'total_price', 'created_at', 'updated_at']
