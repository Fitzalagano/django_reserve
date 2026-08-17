from django.urls import path
from . import views

app_name = 'reservation_app'

urlpatterns = [
    # Customer Routes
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/add/', views.customer_create, name='customer-create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customers/<int:pk>/edit/', views.customer_update, name='customer-update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer-delete'),

    # Table Category Routes
    path('table-categories/', views.table_category_list, name='tablecategory-list'),
    path('table-categories/add/', views.table_category_create, name='tablecategory-create'),
    path('table-categories/<int:pk>/', views.table_category_detail, name='tablecategory-detail'),
    path('table-categories/<int:pk>/edit/', views.table_category_update, name='tablecategory-update'),
    path('table-categories/<int:pk>/delete/', views.table_category_delete, name='tablecategory-delete'),

    # Table Routes
    path('tables/', views.table_list, name='table-list'),
    path('tables/add/', views.table_create, name='table-create'),
    path('tables/<int:pk>/', views.table_detail, name='table-detail'),
    path('tables/<int:pk>/edit/', views.table_update, name='table-update'),
    path('tables/<int:pk>/delete/', views.table_delete, name='table-delete'),

    # Reservation Status Routes
    path('reservation-statuses/', views.reservation_status_list, name='reservationstatus-list'),
    path('reservation-statuses/add/', views.reservation_status_create, name='reservationstatus-create'),
    path('reservation-statuses/<int:pk>/edit/', views.reservation_status_update, name='reservationstatus-update'),

    # Reservation Routes
    path('reservations/', views.reservation_list, name='reservation-list'),
    path('reservations/add/', views.reservation_create, name='reservation-create'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation-detail'),
    path('reservations/<int:pk>/edit/', views.reservation_update, name='reservation-update'),
    path('reservations/<int:pk>/cancel/', views.reservation_cancel, name='reservation-cancel'),

    # Payment Routes
    path('payments/', views.payment_list, name='payment-list'),
    path('payments/add/', views.payment_create, name='payment-create'),
    path('payments/<int:pk>/', views.payment_detail, name='payment-detail'),
    path('payments/<int:pk>/edit/', views.payment_update, name='payment-update'),

    # Audit Log Routes
    path('audit-logs/', views.audit_log_list, name='auditlog-list'),
    path('audit-logs/<int:pk>/', views.audit_log_detail, name='auditlog-detail'),
]