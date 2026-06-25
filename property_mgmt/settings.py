"""
Django settings for property_mgmt project.
DEVELOPMENT ONLY — All production security settings are commented out.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import dj_database_url
except ImportError:
    dj_database_url = None  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env for development
load_dotenv(BASE_DIR / '.env', override=True)

# =============================================================================
# SECURITY
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

DEBUG = True  # DEV ONLY

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*',  # DEV ONLY — allows any host including ngrok
]

# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    'jazzmin',
    'django_q',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
    'django_extensions',
    'widget_tweaks',

    # Custom apps
    'analytics',
    'frontend',
    'properties',
    'transactions',
    'reports',
    'testimonial',
    'subscriptions',
    'payments',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
]

SITE_ID = 1

# =============================================================================
# DJANGO-Q
# =============================================================================

Q_CLUSTER = {
    'name': 'ZiaQ',
    'workers': 2,
    'timeout': 60,
    'retry': 90,
    'queue_limit': 50,
    'orm': 'default',
}

# =============================================================================
# JAZZMIN ADMIN
# =============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "Zia Property Admin",
    "site_header": "Zia Property Dashboard",
    "site_brand": "Zia Properties Ltd",
    "welcome_sign": "Welcome to Zia Admin",
    "copyright": "Zia Properties Ltd",
    "search_model": ["properties.Property"],
    "order_with_respect_to": ["properties", "accounts"],
    "icons": {
        "auth.Group": "fas fa-user-shield",
        "auth.User": "fas fa-user",
        "account.EmailAddress": "fas fa-envelope",
        "account.EmailConfirmation": "fas fa-envelope-open-text",
        "socialaccount.SocialApp": "fas fa-cogs",
        "socialaccount.SocialAccount": "fab fa-facebook-square",
        "socialaccount.SocialToken": "fas fa-key",
        "properties.Agent": "fas fa-user-tie",
        "properties.AgentSubscription": "fas fa-id-badge",
        "properties.Property": "fas fa-home",
        "properties.PropertyImage": "fas fa-image",
        "properties.BuyerLead": "fas fa-user-plus",
        "properties.SellerLead": "fas fa-user-minus",
        "properties.BlogPost": "fas fa-blog",
        "properties.Tenant": "fas fa-users",
        "properties.Lease": "fas fa-file-contract",
        "properties.RentPayment": "fas fa-money-check-alt",
        "properties.MaintenanceRequest": "fas fa-tools",
        "properties.Inspection": "fas fa-search",
        "properties.Payment": "fas fa-money-bill-wave",
        "properties.ContactMessage": "fas fa-envelope-open",
        "reports.IncomeReport": "fas fa-chart-line",
        "subscriptions.PremiumSubscription": "fas fa-crown",
        "subscriptions.MpesaAuditLog": "fas fa-file-invoice-dollar",
        "transactions.Transaction": "fas fa-credit-card",
        "transactions.MpesaTransaction": "fas fa-mobile-alt",
        "testimonial.Testimonial": "fas fa-comment-dots",
        "django_q.Failure": "fas fa-times-circle",
        "django_q.Task": "fas fa-hourglass-alt",
        "django_q.Schedule": "fas fa-calendar-alt",
        "django_q.Success": "fas fa-check-circle",
    },
    "custom_links": {
        "django_q": [{
            "name": "View Q Cluster Logs",
            "url": "/admin/django_q/task/",
            "icon": "fas fa-tasks",
            "permissions": ["django_q.view_task"]
        }],
    },
}

JAZZMIN_UI_TWEAKS = {
    "css": "frontend/custom_dark.css"
}

# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / 'property_mgmt_backend' / 'static',
    BASE_DIR / 'frontend',
]

# DEV ONLY — no whitenoise compression
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# =============================================================================
# MEDIA FILES
# =============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',  # DEV ONLY — commented out
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'subscriptions.middleware.PremiumRequiredMiddleware',
]

premium_paths = [
    "/premium/",
    "/properties/add/",
]

# =============================================================================
# URLS & TEMPLATES
# =============================================================================

ROOT_URLCONF = 'property_mgmt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'property_mgmt.wsgi.application'

# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'zia_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# =============================================================================
# M-PESA SETTINGS
# =============================================================================

MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_BASE_URL = os.getenv("MPESA_BASE_URL", "https://sandbox.safaricom.co.ke")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_SECURITY_CREDENTIAL = os.getenv("MPESA_SECURITY_CREDENTIAL")
MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

# =============================================================================
# EMAIL
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # DEV ONLY — prints to console
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"   # PRODUCTION
# EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@zia-properties.com")

# =============================================================================
# AFRICA'S TALKING
# =============================================================================

AFRICASTALKING_USERNAME = os.getenv("AFRICASTALKING_USERNAME", "")
AFRICASTALKING_API_KEY = os.getenv("AFRICASTALKING_API_KEY", "")

# =============================================================================
# OPENAI
# =============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_WORKFLOW_ID = os.getenv("OPENAI_WORKFLOW_ID", "")

# =============================================================================
# N8N
# =============================================================================

N8N_BASE_URL = os.getenv('N8N_BASE_URL', '')

# =============================================================================
# SECURITY HEADERS — ALL COMMENTED OUT FOR DEV
# =============================================================================

CSRF_TRUSTED_ORIGINS = [
     "https://*.ngrok-free.app",
#     "https://*.onrender.com",
#     "https://ziapropertyagency.com",
#     "https://www.ziapropertyagency.com",
]

# SESSION_COOKIE_SECURE = True        # PRODUCTION ONLY
# CSRF_COOKIE_SECURE = True           # PRODUCTION ONLY
# SECURE_SSL_REDIRECT = True          # PRODUCTION ONLY
# SECURE_BROWSER_XSS_FILTER = True    # PRODUCTION ONLY
# SECURE_CONTENT_TYPE_NOSNIFF = True  # PRODUCTION ONLY
# X_FRAME_OPTIONS = 'DENY'            # PRODUCTION ONLY
# SECURE_HSTS_SECONDS = 31536000      # PRODUCTION ONLY
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # PRODUCTION ONLY
# SECURE_HSTS_PRELOAD = True         # PRODUCTION ONLY

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'dashboard/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/'