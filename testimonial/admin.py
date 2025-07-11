from django.contrib import admin

# Register your models here.
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_visible', 'created_at')
    search_fields = ('name', 'role', 'message')
    list_filter = ('is_visible', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True