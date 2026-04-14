from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from properties.models import Property  # Use your actual app name
import random

def analytics_dashboard(request):
    """Render the analytics HTML page"""
    return render(request, 'frontend/analytics.html')

def get_property_stats(request):
    """API: Overall property statistics"""
    total_properties = Property.objects.count()
    available = Property.objects.filter(is_available=True).count()
    rented = Property.objects.filter(is_available=False).count()  # Assuming rented = not available
    sold = 0  # You don't have sold status, adjust as needed
    
    total_revenue = Property.objects.filter(
        is_available=False
    ).aggregate(Sum('price'))['price__sum'] or 0
    
    avg_price = Property.objects.aggregate(Avg('price'))['price__avg'] or 0
    
    # Calculate occupancy rate (available vs total)
    occupancy_rate = round((available / total_properties * 100), 1) if total_properties > 0 else 0
    
    return JsonResponse({
        'total_properties': total_properties,
        'available': available,
        'rented': rented,
        'sold': sold,
        'occupancy_rate': 100 - occupancy_rate,  # Reverse: not available = occupied
        'total_revenue': float(total_revenue),
        'average_price': float(avg_price),
    })


def get_property_types(request):
    """API: Properties by type for pie chart"""
    data = Property.objects.values('property_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return JsonResponse({
        'labels': [item['property_type'].title() if item['property_type'] else 'Unknown' for item in data],
        'data': [item['count'] for item in data]
    })


def get_monthly_trends(request):
    """API: Listings over last 6 months"""
    months = []
    listings = []
    transactions = []
    
    for i in range(5, -1, -1):
        month_start = timezone.now().replace(day=1) - timedelta(days=i*30)
        month_name = month_start.strftime('%b')
        months.append(month_name)
        
        # New listings that month (using created_at)
        new_listings = Property.objects.filter(
            created_at__month=month_start.month,
            created_at__year=month_start.year
        ).count()
        listings.append(new_listings)
        
        # Transactions (rented/not available)
        trans = Property.objects.filter(
            is_available=False,
            created_at__month=month_start.month,
            created_at__year=month_start.year
        ).count()
        transactions.append(trans)
    
    return JsonResponse({
        'months': months,
        'listings': listings,
        'transactions': transactions
    })


def get_location_data(request):
    """API: Properties by location"""
    locations = Property.objects.values('location').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')[:8]
    
    return JsonResponse({
        'locations': [item['location'] or 'Unknown' for item in locations],
        'counts': [item['count'] for item in locations],
        'avg_prices': [float(item['avg_price']) if item['avg_price'] else 0 for item in locations]
    })


def get_recent_activity(request):
    """API: Recent properties for table"""
    recent = Property.objects.select_related('agent')[:10]
    
    data = [{
        'title': p.property_name,
        'location': p.location or 'N/A',
        'type': p.property_type or 'N/A',
        'price': float(p.price) if p.price else 0,
        'status': 'available' if p.is_available else 'rented',
        'status_display': 'Available' if p.is_available else 'Rented',
        'views': random.randint(10, 500),  # You don't have views_count
        'date': p.created_at.strftime('%Y-%m-%d') if p.created_at else 'N/A'
    } for p in recent]
    
    return JsonResponse({'properties': data})