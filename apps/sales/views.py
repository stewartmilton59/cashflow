from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from .models import Sale

def sales(request):
    # 1. Get the current date in the active timezone
    today = timezone.now().date()
    
    # 2. Filter sales by today's date and calculate aggregated totals
    # The aggregate(Sum('amount')) returns a dictionary: {'amount__sum': total_value}
    cash_query = Sale.objects.filter(timestamp__date=today, payment_method=Sale.PaymentMethods.CASH).aggregate(Sum('amount'))
    phone_query = Sale.objects.filter(timestamp__date=today, payment_method=Sale.PaymentMethods.PHONE).aggregate(Sum('amount'))
    
    # Extract the sum value from the dictionary, defaulting to 0 if no sales exist today
    total_cash_sales = cash_query['amount__sum'] or 0
    total_phone_sales = phone_query['amount__sum'] or 0
    
    # 3. Fetch recent individual transactions for today's logs (ordered newest first)
    recent_sales = Sale.objects.filter(timestamp__date=today).order_by('-timestamp')
    
    # 4. Pass the data into the template context dictionary
    context = {
        'total_cash_sales': total_cash_sales,
        'total_phone_sales': total_phone_sales,
        'recent_sales': recent_sales,
    }
    
    # 5. Render the sales dashboard template with the context data
    return render(request, 'sales/sales.html', context)