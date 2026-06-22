from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Sale
from apps.accounts.models import Account
from apps.core.decorators import accountant_required, director_required


# ── ACCOUNTANT VIEWS ──

@login_required
@accountant_required
def accountant_dashboard(request):
    """
    Accountant dashboard:
    - Shows today's sales for THEIR branch only
    - Form to add new sales (Cash or Phone Payment)
    """
    today = timezone.now().date()

    try:
        account = request.user.account_profile
        user_branch = account.branch
    except Account.DoesNotExist:
        messages.error(request, "Your account profile is not set up.")
        return redirect('login')

    cash_query = Sale.objects.filter(
        timestamp__date=today,
        payment_method=Sale.PaymentMethods.CASH,
        branch=user_branch
    ).aggregate(Sum('amount'))

    phone_query = Sale.objects.filter(
        timestamp__date=today,
        payment_method=Sale.PaymentMethods.PHONE,
        branch=user_branch
    ).aggregate(Sum('amount'))

    total_cash_sales = cash_query['amount__sum'] or 0
    total_phone_sales = phone_query['amount__sum'] or 0
    grand_total_sales = total_cash_sales + total_phone_sales

    branch_sales = Sale.objects.filter(
        timestamp__date=today,
        branch=user_branch
    ).order_by('-timestamp')

    paginator = Paginator(branch_sales, 15)
    page_number = request.GET.get('page', 1)

    try:
        recent_sales = paginator.page(page_number)
    except PageNotAnInteger:
        recent_sales = paginator.page(1)
    except EmptyPage:
        recent_sales = paginator.page(paginator.num_pages)

    context = {
        'branch_name': account.get_branch_display(),
        'branch_code': user_branch,
        'total_cash_sales': total_cash_sales,
        'total_phone_sales': total_phone_sales,
        'grand_total_sales': grand_total_sales,
        'recent_sales': recent_sales,
        'payment_methods': Sale.PaymentMethods.choices,
    }
    return render(request, 'sales/accountant_dashboard.html', context)

@login_required
@accountant_required
def add_sale(request):
    """Handle POST request to add a new sale."""
    if request.method != 'POST':
        return redirect('accountant_dashboard')

    try:
        account = request.user.account_profile
        user_branch = account.branch
    except Account.DoesNotExist:
        messages.error(request, "Your account profile is not set up.")
        return redirect('accountant_dashboard')

    amount_str = request.POST.get('amount', '').strip()
    payment_method = request.POST.get('payment_method', Sale.PaymentMethods.CASH)
    description = request.POST.get('description', '').strip()

    if not amount_str:
        messages.error(request, "Amount is required.")
        return redirect('accountant_dashboard')  

    try:
        amount = float(amount_str)
        if amount <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return redirect('accountant_dashboard')  
    except ValueError:
        messages.error(request, "Invalid amount entered.")
        return redirect('accountant_dashboard')  

    if payment_method not in [Sale.PaymentMethods.CASH, Sale.PaymentMethods.PHONE]:
        messages.error(request, "Invalid payment method.")
        return redirect('accountant_dashboard')  

    Sale.objects.create(
        accountant=request.user,
        branch=user_branch,
        amount=amount,
        payment_method=payment_method,
        description=description,
    )

    messages.success(
        request,
        f"Sale recorded! {payment_method} - {amount:,.2f} Tshs at {account.get_branch_display()}"
    )
    return redirect('accountant_dashboard')  


# ── DIRECTOR VIEWS ──

@login_required
@director_required
def director_dashboard(request):
    """
    Director dashboard:
    - Sees ALL sales from ALL branches
    - Can filter by branch and date range
    - Aggregated metrics per branch
    """
    today = timezone.now().date()

    selected_branch = request.GET.get('branch', '')
    date_from = request.GET.get('date_from', today.strftime('%Y-%m-%d'))
    date_to = request.GET.get('date_to', today.strftime('%Y-%m-%d'))

    sales_qs = Sale.objects.select_related('accountant').all()

    if selected_branch:
        sales_qs = sales_qs.filter(branch=selected_branch)

    if date_from:
        sales_qs = sales_qs.filter(timestamp__date__gte=date_from)
    if date_to:
        sales_qs = sales_qs.filter(timestamp__date__lte=date_to)

    sales_qs = sales_qs.order_by('-timestamp')

    overall_cash = sales_qs.filter(payment_method=Sale.PaymentMethods.CASH).aggregate(Sum('amount'))['amount__sum'] or 0
    overall_phone = sales_qs.filter(payment_method=Sale.PaymentMethods.PHONE).aggregate(Sum('amount'))['amount__sum'] or 0
    overall_total = overall_cash + overall_phone

    branch_totals = []
    for branch_code, branch_name in Sale.BranchChoices.choices:
        branch_sales = sales_qs.filter(branch=branch_code)
        branch_cash = branch_sales.filter(payment_method=Sale.PaymentMethods.CASH).aggregate(Sum('amount'))['amount__sum'] or 0
        branch_phone = branch_sales.filter(payment_method=Sale.PaymentMethods.PHONE).aggregate(Sum('amount'))['amount__sum'] or 0
        branch_total = branch_cash + branch_phone
        transaction_count = branch_sales.count()

        branch_totals.append({
            'code': branch_code,
            'name': branch_name,
            'cash': branch_cash,
            'phone': branch_phone,
            'total': branch_total,
            'transactions': transaction_count,
        })

    paginator = Paginator(sales_qs, 20)
    page_number = request.GET.get('page', 1)

    try:
        recent_sales = paginator.page(page_number)
    except PageNotAnInteger:
        recent_sales = paginator.page(1)
    except EmptyPage:
        recent_sales = paginator.page(paginator.num_pages)

    context = {
        'selected_branch': selected_branch,
        'date_from': date_from,
        'date_to': date_to,
        'branch_choices': Sale.BranchChoices.choices,
        'overall_cash': overall_cash,
        'overall_phone': overall_phone,
        'overall_total': overall_total,
        'branch_totals': branch_totals,
        'recent_sales': recent_sales,
        'total_transactions': sales_qs.count(),
    }
    return render(request, 'sales/director_dashboard.html', context)


@login_required
def sales(request):
    """Legacy sales view - redirects to appropriate dashboard."""
    if request.user.is_director():
        return redirect('sales/director_dashboard.html')
    else:
        return redirect('sales/accountant_dashboard.html')