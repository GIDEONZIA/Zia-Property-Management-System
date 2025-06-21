"""
URL configuration for property_mgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from properties.views import CustomLoginView, dashboard
from django.contrib.auth import views as auth_views
from properties.views import admin_dashboard
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('properties.urls')),  # Make sure 'properties.urls' exists!

    # Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# project/urls.py


urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/', include('transactions.urls')),
]

# project/urls.py (root folder of your project)

def home(request):
    return HttpResponse("Welcome to the Property Management System")

urlpatterns = [
    path('', dashboard, name='dashboard'),
    
    path('admin/', admin.site.urls),
    path('properties/', include('properties.urls')),  # Make sure this line is there
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', include('properties.urls')),
    
    path('reports/', include('reports.urls')),
]


# frontend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
