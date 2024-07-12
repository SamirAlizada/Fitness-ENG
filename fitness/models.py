from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class Trainer(models.Model):
    full_name = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.now)
    monthly_fee = models.IntegerField()
    student_fee = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.full_name}"

class Tariffs(models.Model):
    PRICING_TYPE_CHOICES = [
        ('Daily', 'Daily'),
        ('Monthly', 'Monthly'),
    ]
    
    name = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=10, choices=PRICING_TYPE_CHOICES)
    month_duration = models.IntegerField(null=True, blank=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

class Student(models.Model):
    full_name = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.now)
    tariffs = models.ForeignKey(Tariffs, on_delete=models.CASCADE, null=True, blank=True)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, null=True, blank=True)
    payment = models.IntegerField(default=0)
    end_date = models.DateField(null=True, blank=True)
    is_renewed = models.BooleanField(default=False)

    def calculate_payment(self):
        payment = 0.0  # Initially, the payment is reset

        if self.tariffs is not None:
            payment += self.tariffs.price  # Add the tariff price
            
            if self.tariffs.type == 'Monthly' and self.trainer:
                payment += self.trainer.student_fee * self.tariffs.month_duration
        
        # Update the payment in the `payment` variable
        self.payment = payment

    def calculate_end_date(self):
        # Calculation of end_date by adding months to month_duration on registration_date
        if self.tariffs and self.tariffs.type == 'Monthly':
            self.end_date = self.registration_date + relativedelta(months=self.tariffs.month_duration)

        if self.tariffs and self.tariffs.type == 'Daily':
            self.end_date = self.registration_date

    def save(self, *args, **kwargs):
        # Calculate the payment before saving
        self.calculate_payment()
        self.calculate_end_date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.full_name}"

class Bar(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    stock_number = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.product_name}"
    
class BarSold(models.Model):
    product_name = models.ForeignKey(Bar, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    price = models.FloatField()
    count = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product_name}"