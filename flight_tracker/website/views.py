from django.shortcuts import render    
from django.http import HttpResponse    
from django.template import loader    
from django.shortcuts import redirect    
from django.contrib.auth import authenticate, login, logout    
import hashlib    
import random
import datetime    
import time
import pytz
from django.db import models, connection
from .models import *    
import base64
from django.contrib.auth.models import User 

utc=pytz.UTC


def bleach_sql(s):
    return s.replace(';', '').replace('--', '').replace('/*', '').replace('*/', '').replace('=', '').replace('\'', '').replace('"', '').replace('`', '')

def setup(request):
    with connection.cursor() as cursor:
        cursor.execute(f"""
        DELETE FROM website_airlinestaff WHERE TRUE;
        DELETE FROM website_airline WHERE TRUE;
        DELETE FROM website_airport WHERE TRUE;
        DELETE FROM website_airplane WHERE TRUE;
        """)
        cursor.execute(f"""
        INSERT INTO website_airline (name) VALUES ('Delta');
        INSERT INTO website_airline (name) VALUES ('American Airlines');
        INSERT INTO website_airline (name) VALUES ('United Airlines');
        INSERT INTO website_airline (name) VALUES ('Southwest Airlines');
        INSERT INTO website_airline (name) VALUES ('JetBlue Airways');
        INSERT INTO website_airline (name) VALUES ('Alaska Airlines');
        INSERT INTO website_airline (name) VALUES ('Spirit Airlines');
        INSERT INTO website_airline (name) VALUES ('Frontier Airlines');
        INSERT INTO website_airline (name) VALUES ('Hawaiian Airlines');
        INSERT INTO website_airline (name) VALUES ('Allegiant Air');
        INSERT INTO website_airline (name) VALUES ('Virgin America');
        INSERT INTO website_airline (name) VALUES ('Sun Country Airlines');
        INSERT INTO website_airline (name) VALUES ('WestJet');
        INSERT INTO website_airline (name) VALUES ('Air Canada');
        INSERT INTO website_airline (name) VALUES ('Air France');
        INSERT INTO website_airline (name) VALUES ('British Airways');
        INSERT INTO website_airline (name) VALUES ('Lufthansa');
        INSERT INTO website_airline (name) VALUES ('Qatar Airways');
        INSERT INTO website_airline (name) VALUES ('Singapore Airlines');
        INSERT INTO website_airline (name) VALUES ('Emirates');
        INSERT INTO website_airline (name) VALUES ('KLM');
        """)
        cursor.execute(f"""
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('LAX', 'Los Angeles', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('JFK', 'New York', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('SFO', 'San Francisco', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('ORD', 'Chicago', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('DFW', 'Dallas', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('ATL', 'Atlanta', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('DEN', 'Denver', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('CLT', 'Charlotte', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('SEA', 'Seattle', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('MIA', 'Miami', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('LAS', 'Las Vegas', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('PHX', 'Phoenix', 'US', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('CDG', 'Paris', 'FR', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('HND', 'Tokyo', 'JP', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('LHR', 'London', 'UK', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('PEK', 'Beijing', 'CN', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('FRA', 'Frankfurt', 'DE', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('HKG', 'Hong Kong', 'HK', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('DXB', 'Dubai', 'AE', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('AMS', 'Amsterdam', 'NL', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('CAN', 'Guangzhou', 'CN', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('CGK', 'Jakarta', 'ID', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('SIN', 'Singapore', 'SG', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('ICN', 'Seoul', 'KR', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('MAD', 'Madrid', 'ES', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('DEL', 'New Delhi', 'IN', 'International');
        INSERT INTO website_airport (name, city, country, airport_type) VALUES ('SYD', 'Sydney', 'AU', 'International');
        """)
        cursor.execute(f"""
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0001', 'Lufthansa', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0002', 'Air France', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0003', 'Delta', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0004', 'Delta', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0005', 'American Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0006', 'American Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0007', 'United Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0008', 'United Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0009', 'Southwest Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0010', 'Southwest Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0011', 'JetBlue Airways', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0012', 'JetBlue Airways', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0013', 'Alaska Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0014', 'Alaska Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0015', 'Spirit Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0016', 'Spirit Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0017', 'Frontier Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0018', 'Frontier Airlines', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0019', 'Allegiant Air', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0020', 'Allegiant Air', 220, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0021', 'Hawaiian Airlines', 200, 'Boeing', '2010-01-01');
        INSERT INTO website_airplane (airplane_id, airline_id, seats, manufacturer, date_built) VALUES ('PL0022', 'Hawaiian Airlines', 220, 'Boeing', '2010-01-01');
        """)
    return redirect('index')

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
    for flight in Flight.objects.raw('SELECT * FROM website_flight ORDER BY departure_date DESC'):
        context['flights'].append({
            'airline': flight.airline.name,
            'flight_no': flight.flight_number,
            'origin': flight.departure_airport.name + ' (' + flight.departure_airport.city + ')',
            'destination': flight.arrival_airport.name + ' (' + flight.arrival_airport.city + ')',
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
#    customer = Customer.objects.filter(email=username)
    customer = Customer.objects.raw(f"SELECT * FROM website_customer WHERE email = '{bleach_sql(username)}'")
    print(customer, flush=True)
    print(len(customer), flush=True)
    if len(customer) == 1:
        salt = customer[0].password_salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == customer[0].password_hash:
            request.session['username'] = username
            request.session['type'] = 'customer'
            return redirect('my_flights')
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})

#Try airline staff by username
#    airline_staff = AirlineStaff.objects.filter(username=username)
    airline_staff = AirlineStaff.objects.raw(f"SELECT * FROM website_airlinestaff WHERE username = '{bleach_sql(username)}'")
    if len(airline_staff) == 1:
        salt = airline_staff[0].password_salt
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        if hashed_password == airline_staff[0].password_hash:
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
    if ('email' not in request.POST or
        'password' not in request.POST or
        'confirm_password' not in request.POST or
        'fname' not in request.POST or
        'lname' not in request.POST or
        'dob' not in request.POST or
        'building_number' not in request.POST or
        'street' not in request.POST or
        'city' not in request.POST or
        'state' not in request.POST or
        'phone' not in request.POST or
        'passport_number' not in request.POST or
        'passport_expiration' not in request.POST or
        'country' not in request.POST):
        return render(request, 'website/register.html', {'error_message': 'Please fill in all fields'})
    if '@' not in request.POST['email'] or '.' not in request.POST['email']:
        return render(request, 'website/register.html', {'error_message': 'Please enter a valid email'})
    if request.POST['password'] != request.POST['confirm_password']:
        return render(request, 'website/register.html', {'error_message': 'Passwords do not match'})
    if len(request.POST['phone']) != 10:
        return render(request, 'website/register.html', {'error_message': 'Please enter a valid phone number'})
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM website_customer WHERE email = %s', [request.POST['email']])
        if cursor.fetchone() is not None:
            return render(request, 'website/register.html', {'error_message': 'Email already exists'})

    # Create customer
    salt = "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for i in range(32)])
    hashed_password = hashlib.sha256((request.POST['password'] + salt).encode('utf-8')).hexdigest()
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO website_customer (
                email,
                password_hash,
                password_salt,
                fname,
                lname,
                date_of_birth,
                building_number,
                street,
                city,
                state,
                phone_number,
                passport_number,
                passport_expiration,
                passport_country
                ) VALUES (
                '{bleach_sql(request.POST["email"])}',
                '{bleach_sql(hashed_password)}',
                '{salt}',
                '{bleach_sql(request.POST["fname"])}',
                '{bleach_sql(request.POST["lname"])}',
                '{bleach_sql(request.POST["dob"])}',
                '{bleach_sql(request.POST["building_number"])}',
                '{bleach_sql(request.POST["street"])}',
                '{bleach_sql(request.POST["city"])}',
                '{bleach_sql(request.POST["state"])}',
                '{bleach_sql(request.POST["phone"])}',
                '{bleach_sql(request.POST["passport_number"])}',
                '{bleach_sql(request.POST["passport_expiration"])}',
                '{bleach_sql(request.POST["country"])}'
                )""")
#   customer = Customer(
#           email=request.POST['email'],
#           password_hash=hashed_password,
#           password_salt=salt,
#           fname=request.POST['fname'],
#           lname=request.POST['lname'],
#           date_of_birth=request.POST['dob'],
#           building_number=request.POST['building_number'],
#           street=request.POST['street'],
#           city=request.POST['city'],
#           state=request.POST['state'],
#           phone_number=request.POST['phone'],
#           passport_number=request.POST['passport_number'],
#           passport_expiration=request.POST['passport_expiration'],
#           passport_country=request.POST['country'],
#       )
#   customer.save()
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
        results = Flight.objects.raw(f"""
        SELECT *
        FROM 
            website_flight
            JOIN website_airport AS origin ON website_flight.departure_airport_id = origin.name
            JOIN website_airport AS destination ON website_flight.arrival_airport_id = destination.name
        WHERE
            website_flight.flight_number LIKE '%{bleach_sql(request.GET['q'])}%' OR
            origin.name LIKE '%{bleach_sql(request.GET['q'])}%' OR
            origin.city LIKE '%{bleach_sql(request.GET['q'])}%' OR
            destination.name LIKE '%{bleach_sql(request.GET['q'])}%' OR
            destination.city LIKE '%{bleach_sql(request.GET['q'])}%' OR
            airline_id LIKE '%{bleach_sql(request.GET['q'])}%'
        ORDER BY website_flight.departure_date DESC
        ;
        """)

        for result in results:
            context['flights'].append({
                'airline': result.airline.name,
                'flight_no': result.flight_number,
                'origin': result.departure_airport.name + ' (' + result.departure_airport.city + ')',
                'destination': result.arrival_airport.name + ' (' + result.arrival_airport.city + ')',
                'departure': result.departure_date.date(),
                'arrival': result.arrival_date.date(),
                'status': result.status,
            })
    else:
        sql_string = f"""
            SELECT *
            FROM
                website_flight
                JOIN website_airport AS origin ON website_flight.departure_airport_id = origin.name
                JOIN website_airport AS destination ON website_flight.arrival_airport_id = destination.name
            WHERE
           """ 
        queries = []
        if 'src' in request.GET and request.GET['src'] != '': # Source airport
            queries.append(f"(origin.name LIKE '%{bleach_sql(request.GET['src'])}%' OR origin.city LIKE '%{bleach_sql(request.GET['src'])}%')")
        if 'dest' in request.GET and request.GET['dest'] != '': # Destination airport
            queries.append(f"(destination.name LIKE '%{bleach_sql(request.GET['dest'])}%' OR destination.city LIKE '%{bleach_sql(request.GET['dest'])}%')")
        if 'date' in request.GET and request.GET['date'] != '': # Date
            queries.append(f"(website_flight.departure_date LIKE '%{bleach_sql(request.GET['date'])}%')") #TODO: date
        if 'airline' in request.GET and request.GET['airline'] != '': # Airline
            queries.append(f"(airline_id LIKE '%{bleach_sql(request.GET['airline'])}%')")
        if 'flight_no' in request.GET and request.GET['flight_no'] != '': # Flight number
            queries.append(f"(website_flight.flight_number LIKE '%{bleach_sql(request.GET['flight_no'])}%')")
        sql_string += ' AND '.join(queries)
        sql_string += ' ORDER BY website_flight.departure_date DESC;'
        if len(queries) > 0:
            results = Flight.objects.raw(sql_string)
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
    results = Ticket.objects.raw(f"""
        SELECT *
        FROM website_ticket
        WHERE customer_id = '{request.session['username']}'
        ;
        """)
    print(results, flush=True)
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
    customer = Customer.objects.raw(f"""
    SELECT *
    FROM website_customer
    WHERE email = '{request.session['username']}'
    ;
    """)[0]
    context['fname'] = customer.fname
    context['lname'] = customer.lname

    if request.method == 'GET':
        if 'flight_no' in request.GET and request.GET['flight_no'] != '':
            try:
                flight = Flight.objects.raw(f"""
                    SELECT *
                    FROM website_flight
                    WHERE flight_number = '{bleach_sql(request.GET['flight_no'])}'
                    ;
                    """)[0]
#                print(flight, flush=True)
            except:
                return redirect('index')
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
                flight = Flight.objects.raw(f"""
                SELECT *
                FROM website_flight
                WHERE flight_number = '{bleach_sql(request.POST['flight_no'])}'
                ;
                """)[0]
                if flight is None:
                    return redirect('search')
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
            with connection.cursor() as cursor:
                count = cursor.execute(f"""
                SELECT COUNT(*)
                FROM website_ticket
                WHERE flight_id = '{request.POST['flight_no']}'
                ;
                """)
                count = cursor.fetchone()[0]
                if count >= flight.airplane.seats:
                    print('No seats available', flush=True)
                    return redirect('search')

            #Create ticket
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO website_ticket (sold_price, card_type, card_number, expiration_date, security_code, customer_id, flight_id, purchase_date)
                    VALUES (
                        '{flight.base_price}',
                        'Unknown',
                        '{bleach_sql(request.POST['cc_no'])}',
                        '{bleach_sql(request.POST['exp_date'])}',
                        '{bleach_sql(request.POST['cvv'])}',
                        '{request.session['username']}',
                        '{request.POST['flight_no']}',
                        '{datetime.datetime.now()}')
                    ;
                    """)
#           ticket = Ticket(
#                   flight=flight,
#                   customer=customer,
#                   sold_price=flight.base_price,
#                   card_type='Unknown',
#                   card_number=request.POST['cc_no'],
#                   expiration_date=request.POST['exp_date'],
#                   security_code=request.POST['cvv'],
#                   purchase_date=datetime.datetime.now(),
#                   )
#           ticket.save()
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
                ticket = Ticket.objects.raw(f"""
                    SELECT *
                    FROM website_ticket
                    WHERE ticket_id = '{bleach_sql(request.GET['ticket_id'])}'
                    ;
                    """)[0]
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
            if 'confirm' not in request.POST:
                return redirect('/cancel_trip?ticket_id=' + request.POST['ticket_id'])
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT *
                    FROM website_ticket
                    WHERE ticket_id = '{bleach_sql(request.POST['ticket_id'])}'
                    AND customer_id = '{request.session['username']}'
                    ;
                    """)
                if cursor.rowcount == 0:
                    return redirect('my_flights')
                cursor.execute(f"""
                    DELETE FROM website_ticket
                    WHERE ticket_id = '{bleach_sql(request.POST['ticket_id'])}'
                    ;
                    """)
            return redirect('my_flights')
        else:
            return redirect('my_flights')


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
                ticket = Ticket.objects.raw(f"""
                    SELECT *
                    FROM website_ticket
                    WHERE ticket_id = '{bleach_sql(request.GET['ticket_id'])}'
                    AND customer_id = '{request.session['username']}'
                    ;
                    """)[0]
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
            context['default_rating'] = 5
            return render(request, 'website/rate.html', context)
        elif 'rating_id' in request.GET and request.GET['rating_id'] != '':
            try:
                rating = Rating.objects.raw(f"""
                    SELECT *
                    FROM website_rating
                    WHERE rating_id = '{bleach_sql(request.GET['rating_id'])}'
                    AND customer_id = '{request.session['username']}'
                    ;
                    """)[0]
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
            context['default_rating'] = rating.rating
            return render(request, 'website/rate.html', context)
        else:
            return redirect('my_flights')
    print(request.POST, flush=True)
    if request.method == 'POST':
        if 'ticket_id' in request.POST and request.POST['ticket_id'] != '':
            try:
                ticket = Ticket.objects.raw(f"""
                SELECT *
                FROM website_ticket
                WHERE ticket_id = '{bleach_sql(request.POST['ticket_id'])}'
                AND customer_id = '{request.session['username']}'
                ;
                """)[0]
            except:
                print('ticket not found', flush=True)
                return redirect('my_ratings')
            if Rating.objects.filter(flight=ticket.flight, customer=ticket.customer).exists():
                print('rating already exists')
                return redirect('my_ratings')

            #Create rating object
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO website_rating (rating, comment, customer_id, flight_id)
                    VALUES ({bleach_sql(request.POST['rating'])}, '{bleach_sql(request.POST['comment'])}', '{request.session['username']}', '{ticket.flight.flight_number}')
                    ;
                    """)
#           rating = Rating(
#                   flight=ticket.flight,
#                   rating=request.POST['rating'],
#                   comment=request.POST['comment'],
#                   customer=ticket.customer,
#                   )
#           rating.save()
            return redirect('my_ratings')
        elif 'rating_id' in request.POST and request.POST['rating_id'] != '':
            with connection.cursor() as cursor:
                cursor.execute(f"""
                UPDATE website_rating
                SET rating = {bleach_sql(request.POST['rating'])}, comment = '{bleach_sql(request.POST['comment'])}'
                WHERE rating_id = '{bleach_sql(request.POST['rating_id'])}'
                AND customer_id = '{request.session['username']}'
                ;
                """)
            return redirect('my_ratings')
        else:
            return redirect('my_ratings')

    return render(request, 'website/rate.html', context)

def my_ratings(request):
    context = {}
    context['title'] = 'My Ratings'
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
        ratings = Rating.objects.raw(f"""
        SELECT * FROM website_rating
        WHERE customer_id = '{request.session['username']}'
        ;
        """)
        
        context['ratings'] = []
        for rating in ratings:
            context['ratings'].append({
                'rating': rating.rating,
                'comment': rating.comment,
                'id': rating.rating_id,
                })
        return render(request, 'website/my_ratings.html', context)

def track_spending(request):    
    context = {}
    context['title'] = 'Track Spending'
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

    tickets = Ticket.objects.raw(f"""
    SELECT * FROM website_ticket
    WHERE customer_id = '{request.session['username']}'
    ;
    """)
    context['tickets'] = []
    context['amount_spent'] = 0
    for ticket in tickets:
        context['tickets'].append({
            'ticket_id': ticket.ticket_id,
            'flight_number': ticket.flight.flight_number,
            'airline': ticket.flight.airline.name,
            'purchase_date': datetime.datetime.strftime(ticket.purchase_date, '%Y-%m-%d %H:%M'),
            'departure_date': datetime.datetime.strftime(ticket.flight.departure_date, '%Y-%m-%d %H:%M'),
            'arrival_date': datetime.datetime.strftime(ticket.flight.arrival_date, '%Y-%m-%d %H:%M'),
            'departure_airport': ticket.flight.departure_airport.name,
            'arrival_airport': ticket.flight.arrival_airport.name,
            'price_paid': ticket.sold_price,
            })
        context['amount_spent'] += ticket.sold_price
    return render(request, 'website/track_spending.html', context)

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
    salt = "".join([random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") for i in range(32)])
    hashed_password = hashlib.sha256((request.POST['password'] + salt).encode('utf-8')).hexdigest()
    with connection.cursor() as cursor:
        cursor.execute(f"""
        INSERT INTO website_airlinestaff (
        username,
        password_hash,
        password_salt,
        date_of_birth,
        phone_number,
        email,
        airline_id)
        VALUES (
        '{bleach_sql(request.POST['username'])}',
        '{bleach_sql(hashed_password)}',
        '{bleach_sql(salt)}',
        '{bleach_sql(request.POST['dob'])}',
        '{bleach_sql(request.POST['phone'])}',
        '{bleach_sql(request.POST['email'])}',
        '{bleach_sql(request.POST['airline'])}'
        );
        """)
#   airlinestaff = AirlineStaff(
#           username=request.POST['username'],
#           password_hash=hashed_password,
#           password_salt=salt,
#           date_of_birth=request.POST['dob'],
#           phone_number=request.POST['phone'],
#           email=request.POST['email'],
#           airline=Airline.objects.get(name=request.POST['airline']),
#       )
#   airlinestaff.save()
    return redirect('login')

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
    flights = Flight.objects.raw(f"""
    SELECT *
    FROM website_flight
    WHERE airline_id IN (
    SELECT airline_id FROM website_airlinestaff
    WHERE username = '{request.session['username']}'
    )
    ;
    """)
    for flight in flights:
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT COUNT(*)
            FROM website_ticket
            WHERE flight_id = '{flight.flight_number}'
            """)
            num_tickets = cursor.fetchone()[0]
            cursor.execute(f"""
            SELECT AVG(rating)
            FROM website_rating
            WHERE flight_id = '{flight.flight_number}'
            """)
            avg_rating = cursor.fetchone()[0]
            print(num_tickets, avg_rating, flush=True)
        context['flights'].append({
            'airline': flight.airline.name,
            'flight_no': flight.flight_number,
            'origin': flight.departure_airport.name + ' (' + flight.departure_airport.city + ')',
            'destination': flight.arrival_airport.name + ' (' + flight.arrival_airport.city + ')',
            'departure': flight.departure_date,
            'arrival': flight.arrival_date,
            'ticket_sales': num_tickets,
            'rating': avg_rating,
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
            context['airports'].append(airport.name + ' (' + airport.city + ')')
        for airplane in Airplane.objects.raw(f"""
        SELECT *
        FROM website_airplane
        WHERE airline_id IN (
        SELECT airline_id FROM website_airlinestaff
        WHERE username = '{request.session['username']}'
        )
        ;
        """):
            context['airplanes'].append(airplane.airplane_id)
#            print(context['airplanes'], flush=True)
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT COUNT(*)
            FROM website_flight
            ;
            """)
            num_flights = cursor.fetchone()[0]
        context['flight_no'] = f'FL{num_flights + 1:06d}'
        return render(request, 'website/create_flight.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')

    # Make sure all fields are filled in
    print(request.POST, flush=True)
    for field in request.POST:
        if request.POST[field] == '':
            return redirect('create_flight')
    with connection.cursor() as cursor:
        #(SELECT CONCAT('FL', LPAD(CAST(COUNT(*) + 1 AS CHAR(6)), 6, '0')) FROM website_flight),
        cursor.execute(f""" SELECT COUNT(*) FROM website_flight;""")
        num_flights = cursor.fetchone()[0]
        flight_num = f'FL{num_flights + 1:06d}'
        cursor.execute(f"""
        INSERT INTO website_flight (
        flight_number,
        departure_airport_id,
        arrival_airport_id,
        departure_date,
        arrival_date,
        status,
        airline_id,
        airplane_id,
        base_price
        ) VALUES (
        '{flight_num}',
        '{bleach_sql(request.POST['departure_airport'].split(' (')[0])}',
        '{bleach_sql(request.POST['arrival_airport'].split(' (')[0])}',
        '{bleach_sql(request.POST['departure_date'] + ' ' + request.POST['departure_time'])}',
        '{bleach_sql(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'])}',
        '{bleach_sql(request.POST['status'])}',
        (SELECT airline_id FROM website_airlinestaff WHERE username = '{request.session['username']}'),
        (SELECT id FROM website_airplane WHERE airplane_id = '{bleach_sql(request.POST['airplane'])}'),
        {bleach_sql(request.POST['price'])}
        );
        """)
#   flight = Flight(
#       airline=AirlineStaff.objects.get(username=request.session['username']).airline,
#       flight_number=f'FL{Flight.objects.count() + 1:06d}',
#       departure_airport=Airport.objects.get(name=request.POST['departure_airport']),
#       arrival_airport=Airport.objects.get(name=request.POST['arrival_airport']),
#       departure_date=datetime.datetime.strptime(request.POST['departure_date'] + ' ' + request.POST['departure_time'], '%Y-%m-%d %H:%M'),
#       arrival_date=datetime.datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], '%Y-%m-%d %H:%M'),
#       base_price=request.POST['price'],
#       status=request.POST['status'],
#       airplane=Airplane.objects.get(airplane_id=request.POST['airplane'], airline=AirlineStaff.objects.get(username=request.session['username']).airline),
#   )
#    flight.save()
    return redirect('view_flights')
#    return render(request, 'website/create_flight.html', context)

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
        for airplane in Airplane.objects.raw(f"""
            SELECT *
            FROM website_airplane
            WHERE airline_id IN (
            SELECT airline_id FROM website_airlinestaff
            WHERE username = '{request.session['username']}'
        )
        ;
        """):
            context['airplanes'].append(airplane.airplane_id)
        context['flight_no'] = request.GET['flight_no']
#        flight = Flight.objects.get(flight_number=request.GET['flight_no'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
        flight = Flight.objects.raw(f"""
        SELECT *
        FROM website_flight
        WHERE flight_number = '{request.GET['flight_no']}'
        AND airline_id IN (
        SELECT airline_id FROM website_airlinestaff
        WHERE username = '{request.session['username']}'
        )
        ;
        """)[0]
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
    with connection.cursor() as cursor:
        cursor.execute(f"""
        UPDATE website_flight
        SET
        departure_airport_id = '{bleach_sql(request.POST['departure_airport'])}',
        arrival_airport_id = '{bleach_sql(request.POST['arrival_airport'])}',
        departure_date = '{bleach_sql(request.POST['departure_date'] + ' ' + request.POST['departure_time'])}',
        arrival_date = '{bleach_sql(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'])}',
        status = '{bleach_sql(request.POST['status'])}',
        airplane_id = (SELECT id FROM website_airplane WHERE airplane_id = '{bleach_sql(request.POST['airplane'])}'),
        base_price = {bleach_sql(request.POST['price'])}
        WHERE flight_number = '{bleach_sql(request.POST['flight_no'])}'
        AND airline_id IN (
        SELECT airline_id FROM website_airlinestaff
        WHERE username = '{request.session['username']}'
        )
        ;
        """)
#   flight = Flight.objects.raw(f"""
#   SELECT *
#   FROM website_flight
#   WHERE flight_number = '{request.GET['flight_no']}'
#   AND airline_id IN (
#   SELECT airline_id FROM website_airlinestaff
#   WHERE username = '{request.session['username']}'
#   )
#   ;
#   """)[0]
#   flight.flight_number = request.POST['flight_no']
#   flight.departure_airport=Airport.objects.get(name=request.POST['departure_airport'])
#   flight.arrival_airport=Airport.objects.get(name=request.POST['arrival_airport'])
#   flight.departure_date=datetime.datetime.strptime(request.POST['departure_date'] + ' ' + request.POST['departure_time'], '%Y-%m-%d %H:%M')
#   flight.arrival_date=datetime.datetime.strptime(request.POST['arrival_date'] + ' ' + request.POST['arrival_time'], '%Y-%m-%d %H:%M')
#   flight.base_price=request.POST['price']
#   flight.status=request.POST['status']
#   flight.airplane=Airplane.objects.get(airplane_id=request.POST['airplane'], airline=AirlineStaff.objects.get(username=request.session['username']).airline)
#   flight.save()
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
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT COUNT(*) FROM website_airplane;
            """)
            context['airplane_id'] = f'PL{cursor.fetchone()[0] + 1:04d}'
            context['airplanes'] = cursor.fetchall()
        return render(request, 'website/add_airplane.html', context)
    elif request.method != 'POST':
        return HttpResponse('Invalid request method')

    # Make sure all fields are filled in
    for field in request.POST:
        if request.POST[field] == '':
            return redirect('add_airplane')
    
    with connection.cursor() as cursor:
        cursor.execute(f"""
        SELECT COUNT(*) FROM website_airplane;
        """)
        airplane_id = f'PL{cursor.fetchone()[0] + 1:04d}'
        cursor.execute(f"""
        INSERT INTO website_airplane (
        airplane_id,
        airline_id,
        seats,
        manufacturer,
        date_built
        ) VALUES (
        '{bleach_sql(airplane_id)}',
        (SELECT airline_id FROM website_airlinestaff WHERE username = '{request.session['username']}'),
        {bleach_sql(request.POST['seats'])},
        '{bleach_sql(request.POST['manufacturer'])}',
        '{bleach_sql(request.POST['date_built'])}'
        )
        ;
        """)
#   airplane = Airplane(
#       airplane_id=request.POST['airplane_id'],
#       airline=AirlineStaff.objects.get(username=request.session['username']).airline,
#       seats=request.POST['seats'],
#       manufacturer=request.POST['manufacturer'],
#       date_built=request.POST['date_built'],
#       )
#   airplane.save()
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
        with connection.cursor() as cursor:
            cursor.execute(f"""
            INSERT INTO website_airport (
            name,
            city,
            country,
            airport_type
            ) VALUES (
            '{bleach_sql(request.POST['name'])}',
            '{bleach_sql(request.POST['city'])}',
            '{bleach_sql(request.POST['country'])}',
            '{bleach_sql(request.POST['type'])}'
            )
            ;
            """)
#       airport = Airport(
#           name=request.POST['name'],
#           city=request.POST['city'],
#           country=request.POST['country'],
#           airport_type=request.POST['type'],
#           )
#       airport.save()
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
        ratings = Rating.objects.raw(f"""
        SELECT * FROM website_rating WHERE flight_id IN (
        SELECT flight_id FROM website_flight WHERE flight_number = '{request.GET['flight_no']}' AND airline_id = (SELECT airline_id FROM website_airlinestaff WHERE username = '{request.session['username']}')
        );
        """)
        
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
    context = {}
    context['title'] = 'Frequent Customers'
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

    customers = Customer.objects.all()
    #if no customers:
    if len(customers) == 0:
        return render(request, 'website/view_frequent_customers.html', context)

    context['customers'] = []
    for customer in customers:
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT COUNT(*) FROM website_ticket WHERE customer_id = '{bleach_sql(customer.email)}';
            """)
            total_tickets = cursor.fetchone()[0]
            if total_tickets == 0:
                continue
            #DATE_SUB(NOW(), INTERVAL 1 YEAR)
            cursor.execute(f"""
            SELECT COUNT(*)
            FROM website_ticket JOIN website_flight ON website_ticket.flight_id = website_flight.flight_number
            WHERE
                customer_id = '{bleach_sql(customer.email)}' AND 
                departure_date > '{bleach_sql(str(datetime.datetime.now() - datetime.timedelta(days=30)))}';
            """)
            one_month_tickets = cursor.fetchone()[0]
            cursor.execute(f"""
            SELECT COUNT(*)
            FROM website_ticket JOIN website_flight ON website_ticket.flight_id = website_flight.flight_number
            WHERE
                customer_id = '{bleach_sql(customer.email)}' AND
                departure_date > '{bleach_sql(str(datetime.datetime.now() - datetime.timedelta(days=365)))}';
            """)
            one_year_tickets = cursor.fetchone()[0]
            context['customers'].append({
                'name': customer.fname + ' ' + customer.lname,
                'last_month': one_month_tickets,
                'last_year': one_year_tickets,
                'username': customer.email,
                })
    context['customers'] = sorted(context['customers'], key=lambda x: x['last_year'], reverse=True)
    context['most_frequent'] = context['customers'][0]['name']
    context['most_frequent_flights'] = context['customers'][0]['last_year']

    return render(request, 'website/view_frequent_customers.html', context)

def view_customer_flights(request):
    context = {}
    context['title'] = 'Customer Flights'
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

    if request.method != 'GET':
        return redirect('view_flights')
    if 'customer' not in request.GET or request.GET['customer'] == '':
        return redirect('view_flights')
    tickets = Ticket.objects.raw(f"""
    SELECT * FROM website_ticket WHERE customer_id = '{bleach_sql(request.GET['customer'])}';
    """)
    customer = Customer.objects.raw(f"""
    SELECT * FROM website_customer WHERE email = '{bleach_sql(request.GET['customer'])}';
    """)[0]
    context['flights'] = []
    for ticket in tickets:
        context['flights'].append({
            'flight_no': ticket.flight.flight_number,
            'departure': ticket.flight.departure_airport.name,
            'arrival': ticket.flight.arrival_airport.name,
            'departure_date': ticket.flight.departure_date,
            'arrival_date': ticket.flight.arrival_date,
            'purchase_date': datetime.datetime.strftime(ticket.purchase_date, '%Y-%m-%d'),
            'price': ticket.sold_price,
            })
    context['customer_name'] = customer.fname + ' ' + customer.lname
    return render(request, 'website/view_customer_flights.html', context)
    
def view_reports(request):    
    context = {}
    context['title'] = 'Reports'
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

    #get last 12 months
    now = time.localtime()
    #set now to 2 months ago
    #now = time.localtime(time.mktime((now.tm_year, now.tm_mon-2, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, now.tm_wday, now.tm_yday, now.tm_isdst)))
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    context['months'] = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(12)]
    context['months'] = [str(months[month - 1]) + ' ' + str(year) for (year, month) in context['months']]
    context['months'].reverse()
    print(context['months'], flush=True)

    context['counts'] = [0 for _ in range(12)]
    tickets = Ticket.objects.all()
    for ticket in tickets:
        ticket.month = str(ticket.flight.departure_date.month)
        context['counts'][int(ticket.month) - 1] += 1
    #context['counts'].reverse()
    print(context['counts'], flush=True)

    return render(request, 'website/view_reports.html', context)

def view_earned_revenue(request):    
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

#    tickets = Ticket.objects.filter(flight__airline=AirlineStaff.objects.get(username=request.session['username']).airline)
    tickets = Ticket.objects.raw(f"""
    SELECT *
    FROM website_ticket JOIN website_flight ON website_ticket.flight_id = website_flight.flight_number
    WHERE website_flight.airline_id IN (
        SELECT airline_id FROM website_airlinestaff WHERE username = '{bleach_sql(request.session['username'])}'
        );
    """)
    context['tickets'] = []
    context['total_revenue'] = 0
    context['last_month_revenue'] = 0
    context['last_year_revenue'] = 0
    for ticket in tickets:
        context['tickets'].append({
            'customer_name': ticket.customer.fname + ' ' + ticket.customer.lname,
            'flight_number': ticket.flight.flight_number,
            'purchase_date': datetime.datetime.strftime(ticket.purchase_date, '%Y-%m-%d') + ' ' + datetime.datetime.strftime(ticket.purchase_date, '%H:%M'),
            'departure_date': datetime.datetime.strftime(ticket.flight.departure_date, '%Y-%m-%d %H:%M'),
            'arrival_date': datetime.datetime.strftime(ticket.flight.arrival_date, '%Y-%m-%d %H:%M'),
            'departure_airport': ticket.flight.departure_airport.name,
            'arrival_airport': ticket.flight.arrival_airport.name,
            'price_paid': ticket.sold_price,
            })
        #if purchased within the past 30 days
        if ticket.flight.departure_date > utc.localize(datetime.datetime.now() - datetime.timedelta(days=30)):
            context['last_month_revenue'] += ticket.sold_price
        #if purchased within 365 days
        if ticket.flight.departure_date > utc.localize(datetime.datetime.now() - datetime.timedelta(days=365)):
            context['last_year_revenue'] += ticket.sold_price
        context['total_revenue'] += ticket.sold_price
    return render(request, 'website/view_earned_revenue.html', context)
