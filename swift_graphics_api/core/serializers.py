from rest_framework import serializers
from .models import Service, Order, BusinessCardDesign, EulogyDocument


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
