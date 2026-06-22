from django.shortcuts import render
from .models import Account

def accounts(request):
    # 1. Fetch all account records from the database
    all_accounts = Account.objects.all()
    
    # 2. Fetch the human-readable branch choices to use as a filter menu
    branch_choices = Account.BranchChoices.choices
    
    # 3. Pass everything to the template via the context dictionary
    context = {
        'accounts': all_accounts,
        'branch_choices': branch_choices,
    }
    
    return render(request, 'accounts/accounts.html', context)
