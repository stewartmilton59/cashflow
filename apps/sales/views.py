from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Sale

def sales(request):
    today = timezone.now().date()
    
    # 1. Running dashboard metrics for the entire day (Unchanged)
    cash_query = Sale.objects.filter(timestamp__date=today, payment_method=Sale.PaymentMethods.CASH).aggregate(Sum('amount'))
    phone_query = Sale.objects.filter(timestamp__date=today, payment_method=Sale.PaymentMethods.PHONE).aggregate(Sum('amount'))
    
    total_cash_sales = cash_query['amount__sum'] or 0
    total_phone_sales = phone_query['amount__sum'] or 0
    grand_total_sales = total_cash_sales + total_phone_sales
    
    # 2. Get all today's transactions
    all_today_sales = Sale.objects.filter(timestamp__date=today).order_by('-timestamp')
    
    # 3. Paginate: Show 15 sales per page
    paginator = Paginator(all_today_sales, 15)
    page_number = request.GET.get('page', 1)  # Get current page from URL, default to 1
    
    try:
        recent_sales = paginator.page(page_number)
    except PageNotAnInteger:
        recent_sales = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        recent_sales = paginator.page(paginator.num_pages)  # If page out of range, deliver last
        
    context = {
        'total_cash_sales': total_cash_sales,
        'total_phone_sales': total_phone_sales,
        'grand_total_sales': grand_total_sales,
        'recent_sales': recent_sales,  # This now contains your page items and pagination helpers
    }
    
    return render(request, 'sales/sales.html', context)