# reports/models.py

from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Payment

User = get_user_model()

class IncomeReport(models.Model):
    name = models.CharField(max_length=255)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    number_of_payments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Income Report: {self.name}"

    def save(self, *args, **kwargs):
        # Calculate the total income before saving
        self.total_income = self.calculate_total_income()
        super().save(*args, **kwargs)

    def calculate_total_income(self):
        # Calculate total income by summing related payments in the date range
        payments = Payment.objects.filter(date_paid__range=[self.start_date, self.end_date])
        total = sum(payment.amount for payment in payments)
        self.number_of_payments = payments.count()  # Count payments in date range
        return total
