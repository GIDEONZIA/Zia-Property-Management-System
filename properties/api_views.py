"""DRF ViewSets for n8n automation API endpoints."""
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from .models import (
    Agent, AgentSubscription, Property, Tenant, Lease, RentPayment,
    MaintenanceRequest, Inspection, BuyerLead, SellerLead, BlogPost,
    ContactMessage, Payment
)
from .api_serializers import (
    AgentSerializer, AgentSubscriptionSerializer, PropertySerializer,
    TenantSerializer, LeaseSerializer, RentPaymentSerializer,
    MaintenanceRequestSerializer, InspectionSerializer,
    BuyerLeadSerializer, SellerLeadSerializer, BlogPostSerializer,
    ContactMessageSerializer, PaymentSerializer
)


class LeaseFilter(django_filters.FilterSet):
    end_date__gt = django_filters.DateFilter(field_name='end_date', lookup_expr='gt')
    end_date__in_days = django_filters.CharFilter(method='filter_end_date_in_days')
    rent_payment_status = django_filters.CharFilter(field_name='rent_payment_status')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_terminated = django_filters.BooleanFilter(field_name='is_terminated')

    class Meta:
        model = Lease
        fields = ['is_active', 'rent_payment_status', 'is_terminated']

    def filter_end_date_in_days(self, queryset, name, value):
        try:
            days = [int(d.strip()) for d in value.split(',')]
            today = timezone.now().date()
            q_objects = Q()
            for d in days:
                target = today + timedelta(days=d)
                q_objects |= Q(end_date=target)
            return queryset.filter(q_objects)
        except (ValueError, TypeError):
            return queryset


class PropertyFilter(django_filters.FilterSet):
    updated_at__gte = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    is_available = django_filters.BooleanFilter(field_name='is_available')

    class Meta:
        model = Property
        fields = ['is_available', 'updated_at__gte']


class MaintenanceRequestFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    requested_on__gte = django_filters.DateFilter(field_name='requested_on', lookup_expr='gte')

    class Meta:
        model = MaintenanceRequest
        fields = ['status']


class SubscriptionFilter(django_filters.FilterSet):
    end_date__lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = AgentSubscription
        fields = ['end_date__lte']


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'agency_name']

    @action(detail=True, methods=['post'])
    def flag_review(self, request, pk=None):
        agent = self.get_object()
        agent.is_verified = False
        agent.save()
        return Response({'status': 'flagged_for_review', 'agent_id': agent.id})


class AgentSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = AgentSubscription.objects.all()
    serializer_class = AgentSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubscriptionFilter


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PropertyFilter
    search_fields = ['property_name', 'location', 'address']


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['property_name', 'email', 'phone']


class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LeaseFilter
    search_fields = ['tenant__property_name', 'property__property_name']

    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        lease = self.get_object()
        lease.is_renewed = True
        lease.renewal_date = timezone.now()
        lease.save()
        return Response({'status': 'renewed', 'lease_id': lease.id})

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        lease = self.get_object()
        lease.is_terminated = True
        lease.termination_date = timezone.now()
        lease.is_active = False
        lease.save()
        return Response({'status': 'terminated', 'lease_id': lease.id})


class RentPaymentViewSet(viewsets.ModelViewSet):
    queryset = RentPayment.objects.all()
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tenant', 'lease', 'payment_method']


class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaintenanceRequestFilter

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        maintenance = self.get_object()
        assigned_via = request.data.get('assigned_via', 'manual')
        priority = request.data.get('priority', 'normal')
        maintenance.status = 'in_progress'
        maintenance.save()
        return Response({
            'status': 'assigned',
            'maintenance_id': maintenance.id,
            'assigned_via': assigned_via,
            'priority': priority
        })


class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property', 'status', 'inspection_date']


class BuyerLeadViewSet(viewsets.ModelViewSet):
    queryset = BuyerLead.objects.all()
    serializer_class = BuyerLeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'email', 'preferred_location']


class SellerLeadViewSet(viewsets.ModelViewSet):
    queryset = SellerLead.objects.all()
    serializer_class = SellerLeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'email', 'location']


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
