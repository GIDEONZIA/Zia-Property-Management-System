from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Custom views
from frontend.views import PublicLoginView, mpesa_callback
from properties.views import InternalLoginView, admin_dashboard
from subscriptions.views import premium_agent_page

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Public authentication
    path('login/', PublicLoginView.as_view(), name='public_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Internal (agent/admin) authentication
    path('dashboard/login/', InternalLoginView.as_view(), name='internal_login'),

    # Dashboards
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    # Frontend/public routes
    path('', include('frontend.urls', namespace='frontend')),  # Namespace assigned here

    # App-specific URLs
    path('properties/', include('properties.urls')),
    path('testimonials/', include('testimonial.urls')),
    path('transactions/', include('transactions.urls')),
    path('reports/', include('reports.urls')),
    path('subscriptions/', include('subscriptions.urls')),

    # API Authentication (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # M-Pesa callback
    path('api/mpesa-callback/', mpesa_callback, name='mpesa_callback'),

    # Premium agent landing page
    path('premium-agent/', premium_agent_page, name='premium-agent-page'),
]

# Static/media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
