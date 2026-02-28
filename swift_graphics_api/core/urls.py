from django.urls import path
from .views import (
	RegisterView, LoginView, LogoutView,
	UserProfileView, ChangePasswordView,
	ServiceListCreateView, ServiceDetailView,
	OrderListCreateView, OrderDetailView, OrderStatusUpdateView,
	BusinessCardDesignCreateView, BusinessCardDesignDetailView,
	EulogyDocumentCreateView, EulogyDocumentDetailView,
	DashboardView
)

urlpatterns = [
	path('auth/register/', RegisterView.as_view(), name='register'),
	path('auth/login/', LoginView.as_view(), name='login'),
	path('auth/logout/', LogouView.as_view(), name='logout'),
	path('auth/profile/', UserProfileView.as_view(), name='profile'),
	path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
	path('services/', ServiceListCreateView.as_view(), name='service-list'),
	path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
	path('orders/', OrderListCreateView.as_view(), name='order-list'),
	path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
	path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status'),
	path('orders/<int:order_id>/business-card/', BusinessCardDesignCreateView.as_view(), name='business-card-create'),
	path('business-cards/<int:pk>/', BusinessCardDesignDetailView.as_view(), name='business-card-detail'),
	path('orders/<int:order_id>/eulogy/', EulogyDocumentCreateView.as_view(), name='eulogy-create'),
	path('eulogies/<int:pk>/', EulogyDocumentDetailView.as_view(), name='eulogy-detail'),
	path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
