from django.utils import timezone
from django.db.models import Sum, Count
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
import csv

from .forms import IncomeReportFilterForm
from properties.models import Payment


# 📊 Main Income Report View (With Filtering)
def income_report_view(request):
    form = IncomeReportFilterForm(request.GET or None)
    total_income = number_of_payments = 0
    payments = []

    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        payments = Payment.objects.filter(date__range=(start, end))

        total_income = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        number_of_payments = payments.aggregate(Count('id'))['id__count']

    context = {
        'form': form,
        'total_income': total_income,
        'number_of_payments': number_of_payments,
        'payments': payments,
    }
    return render(request, 'reports/income_report.html', context)


# 📤 CSV Export View
def income_report_csv(request):
    form = IncomeReportFilterForm(request.GET)
    if not form.is_valid():
        return HttpResponse("Invalid filters", status=400)

    start = form.cleaned_data['start_date']
    end = form.cleaned_data['end_date']
    payments = Payment.objects.filter(date__range=(start, end))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="income_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Property'])

    for p in payments:
        writer.writerow([p.date, p.amount, str(p.property)])

    return response


# 📄 PDF Export View
def income_report_pdf(request):
    form = IncomeReportFilterForm(request.GET)
    if not form.is_valid():
        return HttpResponse("Invalid filters", status=400)

    start = form.cleaned_data['start_date']
    end = form.cleaned_data['end_date']
    payments = Payment.objects.filter(date__range=(start, end))
    total_income = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    number_of_payments = payments.count()

    context = {
        'payments': payments,
        'total_income': total_income,
        'number_of_payments': number_of_payments,
        'start': start,
        'end': end,
    }

    template = get_template('reports/income_report_pdf.html')
    html = template.render(context)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

    if pdf.err:
        return HttpResponse("PDF generation error", status=500)

    result = HttpResponse(response.getvalue(), content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="income_report.pdf"'
    return result


# 📋 Report Dashboard View
def report_dashboard(request):
    return render(request, 'reports/dashboard.html')


# 📁 Placeholder Views for Other Reports
def expense_report_view(request):
    return render(request, 'reports/expense_report.html')

def occupancy_report_view(request):
    return render(request, 'reports/occupancy_report.html')

def maintenance_report_view(request):
    return render(request, 'reports/maintenance_report.html')

def agent_performance_report_view(request):
    return render(request, 'reports/agent_performance_report.html')

# Remove or complete the context dictionary
# Example of completing it:
context = {
    'now': timezone.now(),
    'example_key': 'example_value',
}