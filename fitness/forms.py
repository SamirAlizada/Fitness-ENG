from django import forms
from .models import Student, Trainer, Bar, BarSold, Tariffs
from datetime import datetime, date

class CustomDateInput(forms.DateInput):
    input_type = 'text'
    format = '%d/%m/%Y'

    def __init__(self, *args, **kwargs):
        kwargs['format'] = self.format
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if value:
            if isinstance(value, (datetime, date)):
                return value.strftime(self.format)
        return value

class TariffsForm(forms.ModelForm):
    class Meta:
        model = Tariffs
        fields = ['name', 'type', 'month_duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'month_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tariff_type = cleaned_data.get('type')
        month_duration = cleaned_data.get('month_duration')

        if tariff_type == 'Monthly' and not month_duration:
            self.add_error('month_duration', 'Month duration is required for monthly tariffs.')

        if tariff_type == 'Daily' and month_duration:
            self.add_error('month_duration', 'Month duration should be empty for daily tariffs.')

        return cleaned_data

class TrainerForm(forms.ModelForm):
    registration_date = forms.CharField(widget=CustomDateInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Trainer
        fields = ['full_name', 'registration_date', 'monthly_fee', 'student_fee']
        labels = {
            'full_name': 'Ad-Soyad',
            'registration_date': 'Qeydiyyat tarixi',
            'monthly_fee': 'Maaş',
            'student_fee': 'Tələbə Haqqı',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If create new form
            self.fields['registration_date'].initial = date.today().strftime('%d/%m/%Y')
    
    def clean_registration_date(self):
        registration_date = self.cleaned_data['registration_date']
        if isinstance(registration_date, str):
            try:
                return datetime.strptime(registration_date, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError("Enter the date in DD/MM/YYYY format.")
        return registration_date

class StudentForm(forms.ModelForm):
    registration_date = forms.CharField(widget=CustomDateInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = Student
        fields = ['full_name', 'registration_date', 'tariffs', 'trainer', 'is_renewed']
        labels = {
            'full_name': 'Full Name',
            'registration_date': 'Registration Date',
            'tariffs': 'Tariff',
            'trainer': 'Trainer',
            'is_renewed': 'Renew',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If create new form
            self.fields['registration_date'].initial = date.today().strftime('%d/%m/%Y')
    
    def clean_registration_date(self):
        registration_date = self.cleaned_data['registration_date']
        if isinstance(registration_date, str):
            try:
                return datetime.strptime(registration_date, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError("Enter the date in DD/MM/YYYY format")
        return registration_date

class BarForm(forms.ModelForm):
    class Meta:
        model = Bar
        fields = ['product_name', 'price', 'stock_number']
        labels = {
            'product_name': 'Product Name',
            'price': 'Price',
            'stock_number': 'Stock Number',
        }

class BarSoldForm(forms.ModelForm):
    date = forms.CharField(widget=CustomDateInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))

    class Meta:
        model = BarSold
        fields = ['product_name', 'date', 'price', 'count']
        labels = {
            'product_name': 'Product Name',
            'date': 'Date',
            'price': 'Price',
            'count': 'Count',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If create new form
            self.fields['date'].initial = date.today().strftime('%d/%m/%Y')
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if isinstance(date, str):
            try:
                return datetime.strptime(date, '%d/%m/%Y').date()
            except ValueError:
                raise forms.ValidationError("Enter the date in DD/MM/YYYY format")
        return date