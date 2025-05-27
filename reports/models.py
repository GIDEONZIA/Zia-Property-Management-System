    # reports/models.py

from django.db import models
from django.contrib.auth import get_user_model
from properties.models import RentPayment

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
        self.total_income, self.number_of_payments = self.calculate_totals()
        super().save(*args, **kwargs)

    def calculate_totals(self):
        payments = RentPayment.objects.all()

        if self.start_date:
            payments = payments.filter(payment_date__gte=self.start_date)
        if self.end_date:
            payments = payments.filter(payment_date__lte=self.end_date)

        total_income = payments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        number_of_payments = payments.count()

        return total_income, number_of_payments

