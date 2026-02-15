from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            domain_url = 'http://localhost:8000/'
            # Example price IDs (replace with actual Stripe Price IDs)
            prices = {
                'starter': 'price_1starter_test',
                'growth': 'price_1growth_test',
            }
            price_key = request.POST.get('price_key', 'starter')
            price_id = prices.get(price_key, prices['starter'])

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                automatic_tax={'enabled': True},
                billing_address_collection='required', # Required for tax calculation
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})

def success(request):
    return render(request, 'dashboard.html', {'status': 'success'})

def cancel(request):
    return render(request, 'dashboard.html', {'status': 'cancelled'})
