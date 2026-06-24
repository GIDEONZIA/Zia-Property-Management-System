from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from frontend.views import PublicLoginView, AgentLoginView
from properties.views import InternalLoginView
from frontend import views as frontend_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', PublicLoginView.as_view(), name='public_login'),
    path('agent/login/', AgentLoginView.as_view(), name='agent_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/login/', InternalLoginView.as_view(), name='internal_login'),
    path('analytics/', include('analytics.urls')),
    path('', include('frontend.urls', namespace='frontend')),
    path('properties/', include('properties.urls')),
    path('testimonials/', frontend_views.testimonials_view, name='testimonials'),
    path('about/', frontend_views.about_view, name='about'),
    path('transactions/', include('transactions.urls')),
    path('reports/', include('reports.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('payments/', include('payments.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve static and media files in production (Whitenoise handles static)
# Media files served via Django in production (until S3/R2 is configured)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)