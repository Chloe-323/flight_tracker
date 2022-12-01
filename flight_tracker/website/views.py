from django.shortcuts import render    
from django.http import HttpResponse    
from django.template import loader    
from django.shortcuts import redirect    
from django.contrib.auth import authenticate, login, logout    
import hashlib    
import datetime    
from django.db import models    
from .models import *    
from django.contrib.auth.models import User 

def index(request):    
    return render(request, 'website/index.html')

def login(request):    
    return render(request, 'website/login.html')

def logout(request):    
    return render(request, 'website/logout.html')

def register(request):    
    return render(request, 'website/register.html')

def search(request):    
    return render(request, 'website/search.html')

#Customer Use Cases

def my_flights(request):    
    return render(request, 'website/my_flights.html')

def purchase_tickets(request):    
    return render(request, 'website/purchase_tickets.html')

def cancel_trip(request):    
    return render(request, 'website/cancel_trip.html')

def rate(request):    
    return render(request, 'website/rate.html')

def track_spending(request):    
    return render(request, 'website/track_spending.html')

# Airline Staff Use Cases

def view_flights(request):    
    return render(request, 'website/view_flights.html')

def create_flight(request):    
    return render(request, 'website/create_flight.html')

def update_flight(request):    
    return render(request, 'website/update_flight.html')

def add_airplane(request):    
    return render(request, 'website/add_airplane.html')

def add_airport(request):    
    return render(request, 'website/add_airport.html')

def view_ratings(request):    
    return render(request, 'website/view_ratings.html')

def view_frequent_customers(request):    
    return render(request, 'website/view_customers.html')

def view_reports(request):    
    return render(request, 'website/view_reports.html')

def view_earned_revenue(request):    
    return render(request, 'website/view_earned_revenue.html')
