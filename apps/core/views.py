from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Account, User
from apps.core.decorators import accountant_required, director_required


def user_login(request):
    """Custom login view that redirects based on user role."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def user_logout(request):
    """Logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    """Redirect users to their appropriate dashboard based on role."""
    if request.user.is_director():
        return redirect('director_dashboard')
    elif request.user.is_accountant():
        return redirect('accountant_dashboard')
    else:
        raise PermissionDenied("You do not have a valid role assigned.")


@login_required
def accounts_list(request):
    """View all accounts (accessible to both roles)."""
    all_accounts = Account.objects.select_related('user').all()
    branch_choices = Account.BranchChoices.choices

    context = {
        'accounts': all_accounts,
        'branch_choices': branch_choices,
    }
    return render(request, 'accounts/accounts.html', context)