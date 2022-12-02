from django.urls import path           
from . import views                     
                                      
urlpatterns = [                          
    path('', views.index, name='index'),                       
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),

    #Customer Use Cases
    path('my_flights', views.my_flights, name='my_flights'),
    path('purchase_tickets', views.purchase_tickets, name='purchase_tickets'),
    path('cancel_trip', views.cancel_trip, name='cancel_trip'),
    path('rate', views.rate, name='rate'),
    path('track_spending', views.track_spending, name='track_spending'),
    
    # Airline Staff Use Cases
    path('register_staff', views.register_staff, name='register_staff'),
    path('view_flights', views.view_flights, name='view_flights'),
    path('create_flight', views.create_flight, name='create_flight'),
    path('update_flight', views.update_flight, name='update_flight'),
    path('add_airplane', views.add_airplane, name='add_airplane'),
    path('add_airport', views.add_airport, name='add_airport'),
    path('view_ratings', views.view_ratings, name='view_ratings'),
    path('view_frequent_customers', views.view_frequent_customers, name='view_frequent_customers'),
    path('view_reports', views.view_reports, name='view_reports'),
    path('view_earned_revenue', views.view_earned_revenue, name='view_earned_revenue'),
]                    
