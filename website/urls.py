from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services.html', views.services, name='services'),
    path('pricing.html', views.pricing, name='pricing'),
    path('contact.html', views.contact, name='contact'),
]
