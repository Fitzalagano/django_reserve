from django import forms
from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']


class TableCategoryForm(forms.ModelForm):
    class Meta:
        model = TableCategory
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['category', 'table_number', 'capacity', 'location', 'is_active']
        widgets = {
            'capacity': forms.NumberInput(attrs={'min': 1}),
        }


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ['name', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'table', 'reservation_date', 'start_time', 'end_time', 'guests', 'status', 'notes']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'guests': forms.NumberInput(attrs={'min': 1}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests is not None and guests <= 0:
            raise forms.ValidationError("Number of guests must be a positive integer.")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        guests = cleaned_data.get('guests')
        table = cleaned_data.get('table')

        if start_time and end_time and end_time <= start_time:
            self.add_error('end_time', "Reservation end time must be later than start time.")

        if guests and table and guests > table.capacity:
            self.add_error('guests', f"Selected table capacity ({table.capacity}) cannot accommodate {guests} guests.")

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reservation', 'amount', 'payment_method', 'payment_status', 'paid_at', 'transaction_id']
        widgets = {
            'paid_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }