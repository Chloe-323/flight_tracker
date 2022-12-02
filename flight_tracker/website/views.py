from django.shortcuts import render    
from django.http import HttpResponse    
from django.template import loader    
from django.shortcuts import redirect    
from django.contrib.auth import authenticate, login, logout    
import hashlib    
import random
import datetime    
from django.db import models    
from .models import *    
from django.contrib.auth.models import User 

def index(request):    
    try:
        new_airline = Airline(name="Delta")
        new_airline.save()
        new_airplane = Airplane(
            airplane_id="1234",
            airline=new_airline,
            manufacturer="Boeing",
            seats=100,
            date_built=datetime.date(2018, 1, 1)
        )
        new_airplane.save()
        jfk = Airport(
            name="JFK",
            city="New York",
            country="US",
            airport_type="International"
            )
        jfk.save()
        lax = Airport(
            name="LAX",
            city="Los Angeles",
            country="US",
            airport_type="International"
            )
        lax.save()
        new_flight = Flight.objects.create(
            airline=Airline.objects.get(name='Delta'),
            flight_number='1234',
            base_price=100.00,
            airplane=Airplane.objects.get(airplane_id='1234', airline=Airline.objects.get(name='Delta')),
            departure_airport=Airport.objects.get(name='JFK'),
            arrival_airport=Airport.objects.get(name='LAX')
        )
        new_flight.save()
    except:
        pass
    context = {}
    context['title'] = 'Home'
    context['subtitle'] = 'Welcome to the home page'
    context['flights'] = [
        {
            'airline': 'Delta',
            'flight_no': 'DL123',
            'origin': 'SFO',
            'destination': 'LAX',
        }
        ]
    for flight in Flight.objects.all():
        context['flights'].append({
            'airline': flight.airline.name,
            'flight_no': flight.flight_number,
            'origin': flight.departure_airport.name,
            'destination': flight.arrival_airport.name,
        })
    return render(request, 'website/index.html', context)

def login(request):    
    if request.method == 'GET':    
        return render(request, 'website/login.html')
    elif request.method != 'POST':    
        return HttpResponse('Invalid request method')

    username = request.POST['username']
    password = request.POST['password']

#Try customer by email 
    customer = Customer.objects.filter(email=username)
    if customer.exists():
        salt = customer.first().salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == customer.first().password:
            request.session['username'] = username
            request.session['type'] = 'customer'
            return redirect('my_flights')
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})

#Try airline staff by username
    airline_staff = AirlineStaff.objects.filter(username=username)
    if airline_staff.exists():
        salt = airline_staff.first().salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == airline_staff.first().password:
            request.session['username'] = username
            request.session['type'] = 'airline_staff'
            return redirect('view_flights')
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})


def register(request):    
    if request.method == 'GET':    
        return render(request, 'website/register.html')
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')
    
    # Input validation (light)
    if request.POST['password'] != request.POST['confirm_password']:
        return render(request, 'website/register.html', {'error_message': 'Passwords do not match'})
    if Customer.objects.filter(email=request.POST['email']).exists():
        return render(request, 'website/register.html', {'error_message': 'Email already exists'})

    # Make sure all fields are filled in
    for field in request.POST:
        if request.POST[field] == '':
            return render(request, 'website/register.html', {'error_message': 'All fields are required'})

    # Create customer
    salt = "".join([chr(random.randint(0, 255)) for i in range(32)])
    hashed_password = hashlib.sha256((request.POST['password'] + salt).encode('utf-8')).hexdigest()
    customer = Customer(
            email=request.POST['email'],
            password_hash=hashed_password,
            password_salt=salt,
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            date_of_birth=request.POST['dob'],
            building_number=request.POST['building_number'],
            street=request.POST['street'],
            city=request.POST['city'],
            state=request.POST['state'],
            phone_number=request.POST['phone'],
            passport_number=request.POST['passport_number'],
            passport_expiration=request.POST['passport_expiration'],
            passport_country=request.POST['country'],
        )
    customer.save()
    return redirect('login')



def logout(request):    
    #flush session
    request.session.flush()
    return redirect('login')

def search(request):    
    context = {}
    context['title'] = 'Search'
    context['flights'] = []

    results = None

    if 'q' in request.GET and request.GET['q'] != '': #Catch-all query
        results = Flight.objects.filter(
            departure_airport__name__icontains=request.GET['q'] # Departure airport name
        ) | Flight.objects.filter(
            arrival_airport__name__icontains=request.GET['q'] # Arrival airport name
        ) | Flight.objects.filter(
            airline__name__icontains=request.GET['q'] # Airline name
        ) | Flight.objects.filter(
            flight_number__icontains=request.GET['q'] # Flight number
        ) | Flight.objects.filter( # Destination city
            arrival_airport__city__icontains=request.GET['q']
        ) | Flight.objects.filter( # Origin city
            departure_airport__city__icontains=request.GET['q']
        )

        for result in results:
            context['flights'].append({
                'airline': result.airline.name,
                'flight_no': result.flight_number,
                'origin': result.departure_airport.name,
                'destination': result.arrival_airport.name,
            })
    else:
        if 'src' in request.GET and request.GET['src'] != '': # Source airport
            results = Flight.objects.filter(
                    departure_airport__name__icontains=request.GET['src']
                    ) | Flight.objects.filter(
                    departure_airport__city__icontains=request.GET['src']
                    )
        if 'dest' in request.GET and request.GET['dest'] != '': # Destination airport
            if not results:
                results = Flight.objects.filter(
                        arrival_airport__name__icontains=request.GET['dest']
                        ) | Flight.objects.filter(
                        arrival_airport__city__icontains=request.GET['dest']
                        )
            else:
                # Search only in the results of the previous search
                results = results.filter(
                        arrival_airport__name__icontains=request.GET['dest']
                        ) | results.filter(
                        arrival_airport__city__icontains=request.GET['dest']
                        )
        if 'date' in request.GET and request.GET['date'] != '': # Date
            if not results:
                results = Flight.objects.filter(
                        departure_time__date=request.GET['date']
                        )
            else:
                results = results.filter(
                        departure_time__date=request.GET['date']
                        )
        if 'airline' in request.GET and request.GET['airline'] != '': # Airline
            if not results:
                results = Flight.objects.filter(
                        airline__name__icontains=request.GET['airline']
                        )
            else:
                results = results.filter(
                        airline__name__icontains=request.GET['airline']
                        )
        if 'flight_no' in request.GET and request.GET['flight_no'] != '': # Flight number
            if not results:
                results = Flight.objects.filter(
                        flight_number__icontains=request.GET['flight_no']
                        )
            else:
                results = results.filter(
                        flight_number__icontains=request.GET['flight_no']
                        )
        if results:
            for result in results:
                context['flights'].append({
                    'airline': result.airline.name,
                    'flight_no': result.flight_number,
                    'origin': result.departure_airport.name,
                    'destination': result.arrival_airport.name,
                })
    return render(request, 'website/search.html', context)

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

def register_staff(request):    
    return render(request, 'website/register_staff.html')

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
