"""
URL configuration for swift_graphics_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
	return Response({
		'message': 'Welcome to Swift Graphics API',
		'version': '1.0',
		'endpoints': {
			'admin': '/admin/',
			'register': '/api/auth/register/',
			'login': '/api/auth/login/',
			'profile': '/api/auth/profile/',
			'services': '/api/services/',
			'orders': '/api/orders/',
			'dashboard': '/api/dashboard/',
		}
	})

urlpatterns = [
	path('', api_root, name='api-root'),
	path('admin/', admin.site.urls),
	path('api/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

