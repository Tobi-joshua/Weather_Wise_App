from django.urls import path
from . import views

urlpatterns = [
    path('', views.temp_here, name='home'),  # Define a root path pattern
    path('Meteo/', views.temp_here, name='temp_here'),
    path('Meteo/othercountries', views.temp_countries, name='temp_countries'),
]
