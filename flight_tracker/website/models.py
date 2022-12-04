from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
    email = models.EmailField(max_length=254, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    password_hash = models.CharField(max_length=256)
    password_salt = models.CharField(max_length=256)
    building_number = models.CharField(max_length=10)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=10)
    passport_number = models.CharField(max_length=10)
    passport_expiration = models.DateField()
    passport_country = models.CharField(max_length=2)
    date_of_birth = models.DateField()

class Airline(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

class Airport(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=2)
    airport_type = models.CharField(max_length=30)

class Airplane(models.Model):
    airplane_id = models.CharField(max_length=30)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    seats = models.IntegerField()
    manufacturer = models.CharField(max_length=30)
    date_built = models.DateField()
    def age(self):
        return datetime.date.today().year - self.date_built.year
    class Meta:
        unique_together = ('airplane_id', 'airline')

class Flight(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=30, primary_key=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_airport')

    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    status = models.CharField(max_length=30)
    class Meta:
        unique_together = (('airline', 'flight_number'),)

class Ticket(models.Model):
    #auto incrementing id
    ticket_id = models.AutoField(primary_key=True)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    card_type = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    security_code = models.CharField(max_length=4)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

class AirlineStaff(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password_hash = models.CharField(max_length=256)
    password_salt = models.CharField(max_length=256)
    date_of_birth = models.DateField()
    #multiple phone numbers
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
