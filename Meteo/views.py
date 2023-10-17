from _datetime import datetime as dt
import geocoder as geocoder  # allows you to retrieve coordinates of various location
import requests  # allows you to make https request
from django.http import HttpResponse
from django.template import loader
from Meteo.models import Worldcities


def temp_here(request):
    location = geocoder.ip('me').latlng
    current_relativehumidity_hourly, current_temperature_hourly, current_temperature_now, \
        current_windspeed_now = get_temp_speed_RH(location)
    template = loader.get_template('index.html')
    context = {'city': "", 'var1': current_windspeed_now, "var2": current_temperature_now,
               "var3": current_temperature_hourly, "var4": current_relativehumidity_hourly}
    return HttpResponse(template.render(context, request))


def temp_countries(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    location = [random_item.lat, random_item.lng]
    temp = get_temp_by_countries(location)
    city = random_item.city
    template = loader.get_template('index.html')
    context = {'city': city, 'temp': temp}
    return HttpResponse(template.render(context, request))


def get_temp_speed_RH(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    current_time_hour = dt.now().hour
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&" \
                  f"current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m"
    meteo_data = requests.get(api_request).json()
    current_windspeed_now = meteo_data["current"]["windspeed_10m"]
    current_temperature_now = meteo_data["current"]["temperature_2m"]
    current_temperature_hourly = meteo_data["hourly"]["temperature_2m"][current_time_hour]
    current_relativehumidity_hourly = meteo_data["hourly"]["relativehumidity_2m"][current_time_hour]
    return current_relativehumidity_hourly, current_temperature_hourly, current_temperature_now, current_windspeed_now


def get_temp_by_countries(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    current_time_hour = dt.now().hour
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    meteo_data = requests.get(api_request).json()
    current_temperature_hourly = meteo_data["hourly"]["temperature_2m"][current_time_hour]
    return current_temperature_hourly
