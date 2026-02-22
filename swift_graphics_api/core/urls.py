from django.urls import path
from .views import (
    ServiceListCreateView, ServiceDetailView,
    OrderListCreateView, OrderDetailView, OrderStatusUpdateView,
    BusinessCardDesignCreateView, BusinessCardDesignDetailView,
    EulogyDocumentCreateView, EulogyDocumentDetailView,
    DashboardView
)

urlpatterns = [
    # Services
    path('services/', ServiceListCreateView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Orders
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status'),

    # Business Cards
    path('orders/<int:order_id>/business-card/', BusinessCardDesignCreateView.as_view(), name='business-card-create'),
    path('business-cards/<int:pk>/', BusinessCardDesignDetailView.as_view(), name='business-card-detail'),

    # Eulogies
    path('orders/<int:order_id>/eulogy/', EulogyDocumentCreateView.as_view(), name='eulogy-create'),
    path('eulogies/<int:pk>/', EulogyDocumentDetailView.as_view(), name='eulogy-detail'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
