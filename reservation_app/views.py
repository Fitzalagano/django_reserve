from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment, AuditLog
from .forms import CustomerForm, TableCategoryForm, TableForm, ReservationStatusForm, ReservationForm, PaymentForm


# --- CUSTOMER VIEWS ---
def customer_list(request):
    customers = list(Customer.objects.values('id', 'first_name', 'last_name', 'email', 'phone', 'created_at'))
    return JsonResponse({'status': 'success', 'data': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return JsonResponse({
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'phone': customer.phone,
        'created_at': customer.created_at
    })

@csrf_exempt
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            customer = form.save()
            return JsonResponse({'status': 'created', 'id': customer.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = CustomerForm(data, instance=customer)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'updated', 'id': customer.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method in ['POST', 'DELETE']:
        customer.delete()
        return JsonResponse({'status': 'deleted', 'id': pk})
    return HttpResponseNotAllowed(['POST', 'DELETE'])


# --- TABLE CATEGORY VIEWS ---
def table_category_list(request):
    categories = list(TableCategory.objects.values('id', 'name', 'description'))
    return JsonResponse({'status': 'success', 'data': categories})

def table_category_detail(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    return JsonResponse({'id': category.id, 'name': category.name, 'description': category.description})

@csrf_exempt
def table_category_create(request):
    if request.method == 'POST':
        form = TableCategoryForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            cat = form.save()
            return JsonResponse({'status': 'created', 'id': cat.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def table_category_update(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = TableCategoryForm(data, instance=category)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'updated', 'id': category.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def table_category_delete(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    if request.method in ['POST', 'DELETE']:
        category.delete()
        return JsonResponse({'status': 'deleted', 'id': pk})
    return HttpResponseNotAllowed(['POST', 'DELETE'])


# --- TABLE VIEWS ---
def table_list(request):
    tables = list(Table.objects.values('id', 'category_id', 'table_number', 'capacity', 'location', 'is_active'))
    return JsonResponse({'status': 'success', 'data': tables})

def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return JsonResponse({
        'id': table.id,
        'category': table.category.name,
        'table_number': table.table_number,
        'capacity': table.capacity,
        'location': table.location,
        'is_active': table.is_active
    })

@csrf_exempt
def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            tbl = form.save()
            return JsonResponse({'status': 'created', 'id': tbl.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = TableForm(data, instance=table)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'updated', 'id': table.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method in ['POST', 'DELETE']:
        table.delete()
        return JsonResponse({'status': 'deleted', 'id': pk})
    return HttpResponseNotAllowed(['POST', 'DELETE'])


# --- RESERVATION STATUS VIEWS ---
def reservation_status_list(request):
    statuses = list(ReservationStatus.objects.values('id', 'name', 'description', 'is_active'))
    return JsonResponse({'status': 'success', 'data': statuses})

@csrf_exempt
def reservation_status_create(request):
    if request.method == 'POST':
        form = ReservationStatusForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            stat = form.save()
            return JsonResponse({'status': 'created', 'id': stat.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def reservation_status_update(request, pk):
    status_obj = get_object_or_404(ReservationStatus, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = ReservationStatusForm(data, instance=status_obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'updated', 'id': status_obj.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])


# --- RESERVATION VIEWS ---
def reservation_list(request):
    queryset = Reservation.objects.all()
    
    # Filter by Customer
    customer_id = request.GET.get('customer')
    if customer_id:
        queryset = queryset.filter(customer_id=customer_id)
        
    # Filter by Reservation Date
    res_date = request.GET.get('reservation_date')
    if res_date:
        queryset = queryset.filter(reservation_date=res_date)
        
    reservations = list(queryset.values(
        'id', 'customer_id', 'table_id', 'reservation_date', 
        'start_time', 'end_time', 'guests', 'status__name', 'notes'
    ))
    return JsonResponse({'status': 'success', 'data': reservations})

def reservation_detail(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    return JsonResponse({
        'id': res.id,
        'customer': str(res.customer),
        'table': str(res.table),
        'reservation_date': res.reservation_date,
        'start_time': str(res.start_time),
        'end_time': str(res.end_time),
        'guests': res.guests,
        'status': res.status.name,
        'notes': res.notes
    })

@csrf_exempt
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            reservation = form.save()
            # Generate Audit Log
            AuditLog.objects.create(
                reservation=reservation,
                action="CREATED",
                performed_by=request.user.username if request.user.is_authenticated else "System/Guest",
                details=f"Reservation created for {reservation.guests} guests on {reservation.reservation_date}."
            )
            return JsonResponse({'status': 'created', 'id': reservation.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = ReservationForm(data, instance=reservation)
        if form.is_valid():
            form.save()
            # Generate Audit Log
            AuditLog.objects.create(
                reservation=reservation,
                action="UPDATED",
                performed_by=request.user.username if request.user.is_authenticated else "Staff",
                details="Reservation details updated."
            )
            return JsonResponse({'status': 'updated', 'id': reservation.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method in ['POST', 'PATCH']:
        cancelled_status, _ = ReservationStatus.objects.get_or_create(name="CANCELLED")
        reservation.status = cancelled_status
        reservation.save()
        # Generate Audit Log
        AuditLog.objects.create(
            reservation=reservation,
            action="CANCELLED",
            performed_by=request.user.username if request.user.is_authenticated else "Staff",
            details="Reservation marked as CANCELLED."
        )
        return JsonResponse({'status': 'cancelled', 'id': reservation.id})
    return HttpResponseNotAllowed(['POST', 'PATCH'])


# --- PAYMENT VIEWS ---
def payment_list(request):
    queryset = Payment.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        queryset = queryset.filter(reservation_id=reservation_id)
        
    payments = list(queryset.values(
        'id', 'reservation_id', 'amount', 'payment_method', 
        'payment_status', 'paid_at', 'transaction_id'
    ))
    return JsonResponse({'status': 'success', 'data': payments})

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return JsonResponse({
        'id': payment.id,
        'reservation_id': payment.reservation_id,
        'amount': str(payment.amount),
        'payment_method': payment.payment_method,
        'payment_status': payment.payment_status,
        'paid_at': payment.paid_at,
        'transaction_id': payment.transaction_id
    })

@csrf_exempt
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST or json.loads(request.body or '{}'))
        if form.is_valid():
            pay = form.save()
            return JsonResponse({'status': 'created', 'id': pay.id}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method in ['POST', 'PUT']:
        data = request.POST or json.loads(request.body or '{}')
        form = PaymentForm(data, instance=payment)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'updated', 'id': payment.id})
        return JsonResponse({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])


# --- AUDIT LOG VIEWS ---
def audit_log_list(request):
    queryset = AuditLog.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        queryset = queryset.filter(reservation_id=reservation_id)
        
    logs = list(queryset.values('id', 'reservation_id', 'action', 'performed_by', 'action_time', 'details'))
    return JsonResponse({'status': 'success', 'data': logs})

def audit_log_detail(request, pk):
    log = get_object_or_404(AuditLog, pk=pk)
    return JsonResponse({
        'id': log.id,
        'reservation_id': log.reservation_id,
        'action': log.action,
        'performed_by': log.performed_by,
        'action_time': log.action_time,
        'details': log.details
    })