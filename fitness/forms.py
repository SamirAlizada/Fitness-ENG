from django import forms
from .models import Student, Trainer, Bar, BarSold, Tariffs

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
    class Meta:
        model = Trainer
        fields = ['full_name', 'registration_date', 'monthly_fee', 'student_fee']
        labels = {
            'full_name': 'Ad-Soyad',
            'registration_date': 'Qeydiyyat tarixi',
            'monthly_fee': 'Maaş',
            'student_fee': 'Tələbə Haqqı',
        }
        widgets = {
            'registration_date' : forms.DateInput(attrs={'type': 'date'}),
        }

class StudentForm(forms.ModelForm):
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
        widgets = {
            'registration_date' : forms.DateInput(attrs={'type': 'date'}),
        }

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
    class Meta:
        model = BarSold
        fields = ['product_name', 'date', 'price', 'count']
        labels = {
            'product_name': 'Product Name',
            'date': 'Date',
            'price': 'Price',
            'count': 'Count',
        }
        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date'}),
        }