from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TableCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Table Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Table(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(
        TableCategory, 
        on_delete=models.CASCADE, 
        related_name='tables'
    )
    table_number = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} ({self.location}) - Cap: {self.capacity}"


class ReservationStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Reservation Statuses"
        ordering = ['name']

    def __str__(self):
        return self.name


class Reservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    table = models.ForeignKey(
        Table, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.ForeignKey(
        ReservationStatus, 
        on_delete=models.PROTECT, 
        related_name='reservations'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reservation_date', '-start_time']

    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({'end_time': "End time must be later than start time."})
        if self.guests and self.table and self.guests > self.table.capacity:
            raise ValidationError({'guests': f"Guest count ({self.guests}) exceeds table capacity ({self.table.capacity})."})

    def __str__(self):
        return f"Reservation #{self.id} - {self.customer} on {self.reservation_date}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    id = models.BigAutoField(primary_key=True)
    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    paid_at = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} - Res #{self.reservation_id} ({self.payment_status})"


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.CASCADE, 
        related_name='audit_logs'
    )
    action = models.CharField(max_length=100)
    performed_by = models.CharField(max_length=100)
    action_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-action_time']

    def __str__(self):
        return f"AuditLog: {self.action} on Res #{self.reservation_id} at {self.action_time}"