from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment, AuditLog

admin.site.register([Customer, TableCategory, Table, ReservationStatus, Reservation, Payment, AuditLog])