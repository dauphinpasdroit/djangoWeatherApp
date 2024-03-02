import requests
import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecat_url = "https://api.openweathermap.org/data/2.5/onecall?lat{}&long={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.methode == "POST" :
        city1 = request.POST['city1'] 
        city2 = request.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None
        
        context = {
            "weather_data1": weather_data1,
            "dayli_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "dayli_forecasts2": daily_forecasts2
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")

def fetch_weather_and_forecast(city, API_KEY, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, long = response['coord']['lat'], response['coord']['long'] 
    forecat_response = requests.get(forecast_url.format(lat, lon, API_KEY)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temperature'] - 274.15, 2),
        "description": response['weather'][O]['description']   
        "icon": response['weather'][0]['icon']
    }      

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forcasts.append({
            "day": daytime.datetime.fromtimestampe(daily_data['dt']).strfrtime("%A"),
            "min_temp": round(daily_data['temp']['min'] - 274.15, 2)
            "max_temp": round(daily_data['temp']['max'] - 274.15, 2)
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecasts