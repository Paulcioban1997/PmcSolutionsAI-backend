from django.contrib import admin
from django.urls import path, include

from quotes import views as quote_views
from dashboard import views as dash_views
from payments import views as stripe_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')), # Assuming website app handles landing page
    path('dashboard/', dash_views.home, name='dashboard'),
    path('quote/', quote_views.quote_page, name='quote-page'),
    path('submit-quote/', quote_views.submit_quote, name='submit-quote'),
    path('create-checkout-session/', stripe_views.create_checkout_session, name='stripe-checkout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ai/', include('ai_engine.urls')),
]
