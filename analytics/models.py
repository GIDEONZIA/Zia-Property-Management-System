from django.db import models
from properties.models import Property

# Add analytics methods to existing Property model via proxy
class PropertyAnalytics(Property):
    class Meta:
        proxy = True
        verbose_name = "Property Analytics"
        verbose_name_plural = "Property Analytics"