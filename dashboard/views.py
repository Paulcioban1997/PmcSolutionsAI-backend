from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def home(request):
    user = request.user
    subscription_status = 'Free Plan' # replace with DB logic
    
    context = {
        'user': user,
        'subscription': subscription_status,
        # Fetch active agents, invoices, etc.
    }
    return render(request, 'dashboard.html', context)
