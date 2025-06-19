from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('create/', views.create_transaction, name='create_transaction'),
    path('list/', views.transaction_list, name='transaction_list'),
    path('update_status/<int:transaction_id>/', views.update_transaction_status, name='update_transaction_status'),
]
