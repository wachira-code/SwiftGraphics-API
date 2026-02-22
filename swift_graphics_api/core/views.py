from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Service, Order, BusinessCardDesign, EulogyDocument
from .serializers import (
    ServiceSerializer, OrderSerializer,
    BusinessCardDesignSerializer, EulogyDocumentSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only admins can create/edit services."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# ── SERVICE VIEWS ──────────────────────────────

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_available=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

