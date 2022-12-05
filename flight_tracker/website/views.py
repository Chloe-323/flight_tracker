from django.shortcuts import render    
from django.http import HttpResponse    
from django.template import loader    
from django.shortcuts import redirect    
from django.contrib.auth import authenticate, login, logout    
import hashlib    
import random
import datetime    
import pytz
from django.db import models    
from .models import *    
from django.contrib.auth.models import User 

utc=pytz.UTC

def index(request):    
    context = {}
    context['title'] = 'Home'
    context['subtitle'] = 'Welcome to the home page'
    context['flights'] = [
        ]
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    for flight in Flight.objects.all():
        context['flights'].append({
            'airline': flight.airline.name,
            'flight_no': flight.flight_number,
            'origin': flight.departure_airport.name,
            'destination': flight.arrival_airport.name,
            'departure': flight.departure_date.date(),
            'arrival': flight.arrival_date.date(),
            'price': flight.base_price,
            'status': flight.status,
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
        salt = customer.first().password_salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == customer.first().password_hash:
            request.session['username'] = username
            request.session['type'] = 'customer'
            return redirect('my_flights')
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})

#Try airline staff by username
    airline_staff = AirlineStaff.objects.filter(username=username)
    if airline_staff.exists():
        salt = airline_staff.first().password_salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == airline_staff.first().password_hash:
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

#TODO: make this raw SQL queries because FINAL PROJECT NEEDS SQL 
def search(request):    
    context = {}
    context['title'] = 'Search'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'


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
                'departure': result.departure_date.date(),
                'arrival': result.arrival_date.date(),
                'status': result.status,
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
                        departure_date__date=request.GET['date']
                        )
            else:
                results = results.filter(
                        departure_date__date=request.GET['date']
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
                    'departure': result.departure_date.date(),
                    'arrival': result.arrival_date.date(),
                    'status': result.status,
                })
    return render(request, 'website/search.html', context)

#Customer Use Cases

def my_flights(request):    
    context = {}
    context['title'] = 'My Flights'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'customer':
        return redirect('login')

    #Get all flights for which the customer has a ticket
    results = Ticket.objects.filter(
            customer__email=request.session['username']
            )
    for result in results:
        context['flights'].append({
            'airline': result.flight.airline.name,
            'flight_no': result.flight.flight_number,
            'origin': result.flight.departure_airport.name,
            'destination': result.flight.arrival_airport.name,
            'departure': result.flight.departure_date,
            'arrival': result.flight.arrival_date,
            'price': result.sold_price,
            'status': result.flight.status,
            'ticket_id': result.ticket_id,
            'ratable': result.flight.arrival_date < utc.localize(datetime.datetime.now()),
        })
    return render(request, 'website/my_flights.html', context)

def purchase_tickets(request):    
    context = {}
    context['title'] = 'Purchase Tickets'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'customer':
        return redirect('login')

    #Find fname and lname of customer
    customer = Customer.objects.get(email=request.session['username'])
    context['fname'] = customer.fname
    context['lname'] = customer.lname

    if request.method == 'GET':
        if 'flight_no' in request.GET and request.GET['flight_no'] != '':
            try:
                flight = Flight.objects.get(
                        flight_number=request.GET['flight_no']
                        )
#                print(flight, flush=True)
            except:
                return redirect('search')
            context['flight'] = {
                'airline': flight.airline.name,
                'flight_no': flight.flight_number,
                'origin': flight.departure_airport.name,
                'destination': flight.arrival_airport.name,
                'departure': flight.departure_date.date(),
                'arrival': flight.arrival_date.date(),
                'price': flight.base_price,
                'status': flight.status,
            }
            return render(request, 'website/purchase_tickets.html', context)
        else:
            return redirect('search')
    elif request.method == 'POST':
        if 'flight_no' in request.POST and request.POST['flight_no'] != '':
            try:
                flight = Flight.objects.get(
                        flight_number=request.POST['flight_no']
                        )
            except:
                return redirect('search')
            #Validate CC info
            if 'cc_no' not in request.POST or request.POST['cc_no'] == '':
                print('No CC number', flush=True)
                return redirect('search')
            if 'exp_date' not in request.POST or request.POST['exp_date'] == '':
                print('No CC exp date', flush=True)
                return redirect('search')
            if 'cvv' not in request.POST or request.POST['cvv'] == '':
                print('No CC cvv', flush=True)
                return redirect('search')

            #Create ticket
            ticket = Ticket(
                    flight=flight,
                    customer=customer,
                    sold_price=flight.base_price,
                    card_type='Unknown',
                    card_number=request.POST['cc_no'],
                    expiration_date=request.POST['exp_date'],
                    security_code=request.POST['cvv'],
                    purchase_time=datetime.datetime.now(),
                    purchase_date=datetime.datetime.today(),
                    )
            ticket.save()
            return redirect('my_flights')
        else:
            return redirect('search')
    return redirect('index')

def cancel_trip(request):    
    context = {}
    context['title'] = 'Cancel Trip'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'customer':
        return redirect('login')

    if request.method == 'GET':
        print(request, flush=True)
        if 'ticket_id' in request.GET and request.GET['ticket_id'] != '':
            try:
                ticket = Ticket.objects.get(
                        ticket_id=request.GET['ticket_id']
                        )
            except:
                return redirect('my_flights')
            context['flight'] = {
                'airline': ticket.flight.airline.name,
                'flight_no': ticket.flight.flight_number,
                'origin': ticket.flight.departure_airport.name,
                'destination': ticket.flight.arrival_airport.name,
                'departure': ticket.flight.departure_date.date(),
                'arrival': ticket.flight.arrival_date.date(),
                'price': ticket.sold_price,
                'status': ticket.flight.status,
                'ticket_id': ticket.ticket_id,
            }
            return render(request, 'website/cancel_trip.html', context)
        else:
            return redirect('my_flights')
    elif request.method == 'POST':
        if 'ticket_id' in request.POST and request.POST['ticket_id'] != '':
            try:
                ticket = Ticket.objects.get(
                        ticket_id=request.POST['ticket_id']
                        )
            except:
                return redirect('my_flights')
            if ticket.customer.email != request.session['username']:
                return redirect('my_flights')
            if 'confirm' not in request.POST:
                context['flight'] = {
                    'airline': ticket.flight.airline.name,
                    'flight_no': ticket.flight.flight_number,
                    'origin': ticket.flight.departure_airport.name,
                    'destination': ticket.flight.arrival_airport.name,
                    'departure': ticket.flight.departure_date.date(),
                    'arrival': ticket.flight.arrival_date.date(),
                    'price': ticket.sold_price,
                    'status': ticket.flight.status,
                    'ticket_id': ticket.ticket_id,
                }
                return render(request, 'website/cancel_trip.html', context)
            ticket.delete()
            return redirect('my_flights')
        else:
            return redirect('my_flights')

    return render(request, 'website/cancel_trip.html')

def rate(request):    
    context = {}
    context['title'] = 'Rate Trip'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'customer':
        return redirect('login')

    if request.method == 'GET':
        if 'ticket_id' in request.GET and request.GET['ticket_id'] != '':
            try:
                ticket = Ticket.objects.get(
                        ticket_id=request.GET['ticket_id']
                        )
            except:
                return redirect('my_flights')
            context['flight'] = {
                'airline': ticket.flight.airline.name,
                'flight_no': ticket.flight.flight_number,
                'origin': ticket.flight.departure_airport.name,
                'destination': ticket.flight.arrival_airport.name,
                'departure': ticket.flight.departure_date.date(),
                'arrival': ticket.flight.arrival_date.date(),
                'price': ticket.sold_price,
                'status': ticket.flight.status,
                'ticket_id': ticket.ticket_id,
            }
        elif 'rating_id' in request.GET and request.GET['rating_id'] != '':
            try:
                rating = Rating.objects.get(
                        rating_id=request.GET['rating_id']
                        )
                flight = rating.flight
            except:
                return redirect('my_flights')
            context['rating_id'] = rating.rating_id
            context['rating'] = {
                'score': rating.rating,
                'comment': rating.comment,
            }
            context['flight'] = {
                'airline': flight.airline.name,
                'flight_no': flight.flight_number,
                'origin': flight.departure_airport.name,
                'destination': flight.arrival_airport.name,
                'departure': flight.departure_date.date(),
                'arrival': flight.arrival_date.date(),
                'status': flight.status,
            }
            return render(request, 'website/rate.html', context)
        else:
            return redirect('my_flights')
    print(request.POST, flush=True)
    if request.method == 'POST':
        if 'ticket_id' in request.POST and request.POST['ticket_id'] != '':
            try:
                ticket = Ticket.objects.get(
                        ticket_id=request.POST['ticket_id']
                        )
            except:
                return redirect('my_flights')
            if ticket.customer.email != request.session['username']:
                return redirect('my_flights')
            #Create rating object
            rating = Rating(
                    flight=ticket.flight,
                    rating=request.POST['rating'],
                    comment=request.POST['comment'],
                    customer=ticket.customer,
                    )
            rating.save()
            return redirect('my_flights')
        else:
            return redirect('my_flights')

    return render(request, 'website/rate.html', context)

def my_ratings(request):
    context = {}
    context['title'] = 'Rate Trip'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'customer':
        return redirect('login')

    if request.method == 'GET':
        customer = Customer.objects.get(email=request.session['username'])
        ratings = Rating.objects.filter(customer=customer)
        
        context['ratings'] = []
        for rating in ratings:
            context['ratings'].append({
                'rating': rating.rating,
                'comment': rating.comment,
                'id': rating.rating_id,
                })
        return render(request, 'website/my_ratings.html', context)

def track_spending(request):    
    return render(request, 'website/track_spending.html')

# Airline Staff Use Cases

def register_staff(request):    
    if request.method == 'GET':    
        context = {}
        context['title'] = 'Register Staff'
        context['airlines'] = []
        for airline in Airline.objects.all():
            print(airline.name, flush=True)
            context['airlines'].append(airline.name)
        return render(request, 'website/register_staff.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')
    
    # Input validation (light)
    if request.POST['password'] != request.POST['confirm_password']:
        return render(request, 'website/register_staff.html', {'error_message': 'Passwords do not match'})
    if AirlineStaff.objects.filter(username=request.POST['username']).exists():
        return render(request, 'website/register_staff.html', {'error_message': 'Email already exists'})

    # Make sure all fields are filled in
    for field in request.POST:
        if request.POST[field] == '':
            return render(request, 'website/register_staff.html', {'error_message': 'All fields are required'})

    # Create customer
    salt = "".join([chr(random.randint(0, 255)) for i in range(32)])
    hashed_password = hashlib.sha256((request.POST['password'] + salt).encode('utf-8')).hexdigest()
    airlinestaff = AirlineStaff(
            username=request.POST['username'],
            password_hash=hashed_password,
            password_salt=salt,
            date_of_birth=request.POST['dob'],
            phone_number=request.POST['phone'],
            email=request.POST['email'],
            airline=Airline.objects.get(name=request.POST['airline']),
        )
    airlinestaff.save()
    return redirect('login')
    return render(request, 'website/register_staff.html')

def view_flights(request):    
    context = {}
    context['title'] = 'View Airline Flights'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')

    # Find all flights operated by the airline
    airline = AirlineStaff.objects.get(username=request.session['username']).airline
    for flight in Flight.objects.filter(airline=airline):
        context['flights'].append({
            'airline': flight.airline.name,
            'flight_no': flight.flight_number,
            'origin': flight.departure_airport.name,
            'destination': flight.arrival_airport.name,
            'departure': flight.departure_date,
            'arrival': flight.arrival_date,
            'ticket_sales': Ticket.objects.filter(flight=flight).count(),
            'rating': Rating.objects.filter(flight=flight).aggregate(models.Avg('rating'))['rating__avg'],
            'status': flight.status,
        })
    return render(request, 'website/view_flights.html', context)

def create_flight(request):    
    context = {}
    context['title'] = 'Create Flight'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')

    if request.method == 'GET':
        context['airports'] = []
        context['airplanes'] = []
        for airport in Airport.objects.all():
            context['airports'].append(airport.name)
        for airplane in Airplane.objects.filter(airline=AirlineStaff.objects.get(username=request.session['username']).airline):
            print(airplane.airplane_id, flush=True)
            context['airplanes'].append(airplane.airplane_id)
            print(context['airplanes'], flush=True)
        context['flight_no'] = f'FL{Flight.objects.count() + 1:04d}'
        return render(request, 'website/create_flight.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')

    # Make sure all fields are filled in
    print(request.POST, flush=True)
    for field in request.POST:
        if request.POST[field] == '':
            return redirect('create_flight')
    flight = Flight(
        airline=AirlineStaff.objects.get(username=request.session['username']).airline,
        flight_number=f'{Flight.objects.count() + 1:04d}',
        departure_airport=Airport.objects.get(name=request.POST['departure_airport']),
        arrival_airport=Airport.objects.get(name=request.POST['arrival_airport']),
        departure_date=datetime.datetime.strptime(request.POST['departure_date'] + ' ' + request.POST['departure_time'], '%Y-%m-%d %H:%M'),
        arrival_date=datetime.datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], '%Y-%m-%d %H:%M'),
        base_price=request.POST['price'],
        status=request.POST['status'],
        airplane=Airplane.objects.get(airplane_id=request.POST['airplane'], airline=AirlineStaff.objects.get(username=request.session['username']).airline),
    )
    flight.save()
    return redirect('view_flights')
    return render(request, 'website/create_flight.html', context)

def update_flight(request):    
    context = {}
    context['title'] = 'Update Flight'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')
    if request.method == 'GET':
        if 'flight_no' not in request.GET:
            return redirect('view_flights')
        if 'airline' not in request.GET:
            return redirect('view_flights')
        context['airports'] = []
        context['airplanes'] = []
        for airport in Airport.objects.all():
            context['airports'].append(airport.name)
        for airplane in Airplane.objects.filter(airline=AirlineStaff.objects.get(username=request.session['username']).airline):
            context['airplanes'].append(airplane.airplane_id)
        context['flight_no'] = request.GET['flight_no']
        flight = Flight.objects.get(flight_number=request.GET['flight_no'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
        context['departure_airport'] = flight.departure_airport.name
        context['arrival_airport'] = flight.arrival_airport.name
        context['departure_date'] = flight.departure_date.strftime('%Y-%m-%d')
        context['departure_time'] = flight.departure_date.strftime('%H:%M')
        context['arrival_date'] = flight.arrival_date.strftime('%Y-%m-%d')
        context['arrival_time'] = flight.arrival_date.strftime('%H:%M')
        context['price'] = flight.base_price
        context['status'] = flight.status
        context['airplane_id'] = flight.airplane.airplane_id
        return render(request, 'website/update_flight.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')

    # Make sure all fields are filled in
    for field in request.POST:
        if request.POST[field] == '':
            return redirect('update_flight')
    flight = Flight.objects.get(flight_number=request.POST['flight_no'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
    flight.flight_number = request.POST['flight_no']
    flight.departure_airport=Airport.objects.get(name=request.POST['departure_airport'])
    flight.arrival_airport=Airport.objects.get(name=request.POST['arrival_airport'])
    flight.departure_date=datetime.datetime.strptime(request.POST['departure_date'] + ' ' + request.POST['departure_time'], '%Y-%m-%d %H:%M')
    flight.arrival_date=datetime.datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], '%Y-%m-%d %H:%M')
    flight.base_price=request.POST['price']
    flight.status=request.POST['status']
    flight.airplane=Airplane.objects.get(airplane_id=request.POST['airplane'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
    flight.save()
    return redirect('view_flights')

def add_airplane(request):    
    context = {}
    context['title'] = 'Add Airplane'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')

    if request.method == 'GET':
        context['airplane_id'] = f'PL{Airplane.objects.count() + 1:08d}'
        return render(request, 'website/add_airplane.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')

    # Make sure all fields are filled in
    for field in request.POST:
        if request.POST[field] == '':
            return redirect('add_airplane')
    
    airplane = Airplane(
        airplane_id=request.POST['airplane_id'],
        airline=AirlineStaff.objects.get(username=request.session['username']).airline,
        seats=request.POST['seats'],
        manufacturer=request.POST['manufacturer'],
        date_built=request.POST['date_built'],
        )
    airplane.save()
    return redirect('create_flight')
    return render(request, 'website/add_airplane.html', context)

def add_airport(request):    
    context = {}
    context['title'] = 'Add Airport'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')

    if request.method == 'POST':
        # Make sure all fields are filled in
        for field in request.POST:
            if request.POST[field] == '':
                return redirect('add_airport')
        airport = Airport(
            name=request.POST['name'],
            city=request.POST['city'],
            country=request.POST['country'],
            airport_type=request.POST['type'],
            )
        airport.save()
        return redirect('create_flight')
    return render(request, 'website/add_airport.html', context)

def view_ratings(request):    
    context = {}
    context['title'] = 'Ratings'
    context['flights'] = []
    if request.session.get('username') is not None:
        context['username'] = request.session['username']
        if request.session['type'] == 'customer':
            context['type'] = 'customer'
        elif request.session['type'] == 'airline_staff':
            context['type'] = 'airline_staff'
        else:
            context['type'] = 'error'
    else:
        return redirect('login')
    if context['type'] != 'airline_staff':
        return redirect('login')

    if request.method == 'GET':
        if 'flight_no' not in request.GET or request.GET['flight_no'] == '':
            return redirect('view_flights')
        flight = Flight.objects.get(flight_number=request.GET['flight_no'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
        ratings = Rating.objects.filter(flight=flight)
        
        context['ratings'] = []
        context['flight_no'] = flight.flight_number
        for rating in ratings:
            context['ratings'].append({
                'rating': rating.rating,
                'comment': rating.comment,
                })
        return render(request, 'website/view_ratings.html', context)
    return render(request, 'website/view_ratings.html', context)

def view_frequent_customers(request):    
    return render(request, 'website/view_customers.html')

def view_reports(request):    
    return render(request, 'website/view_reports.html')

def view_earned_revenue(request):    
    return render(request, 'website/view_earned_revenue.html')
