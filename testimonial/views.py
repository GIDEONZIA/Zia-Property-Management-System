from django.shortcuts import render

# Create your views here.
from .models import Testimonial

def testimonial_view(request):
    testimonials = Testimonial.objects.filter(is_visible=True).order_by('-created_at')
    return render(request, 'frontend/testimonial.html', {'testimonials': testimonials})
