from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Quote
import json

@csrf_exempt
def submit_quote(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            quote = Quote.objects.create(
                name=data.get('name'),
                company=data.get('company'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                service=data.get('service'),
                description=data.get('description'),
            )
            
            # Send email notification (Console backend for now)
            try:
                send_mail(
                    subject=f"Nouvelle demande de soumission: {quote.company}",
                    message=f"""
                    Nouvelle demande reçue !
                    
                    Nom: {quote.name}
                    Compagnie: {quote.company}
                    Email: {quote.email}
                    Téléphone: {quote.phone}
                    Service: {quote.service}
                    
                    Description:
                    {quote.description}
                    """,
                    from_email=settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@pmcsolutionsai.com',
                    recipient_list=['paulmircea15@gmail.com'],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email error: {e}")

            return JsonResponse({"status": "success", "message": "Soumission reçue !"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def quote_page(request):
    return render(request, 'request-quote.html')
