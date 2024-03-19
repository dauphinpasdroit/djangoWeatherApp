import requests
import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = "21c58a2e0167908e6159300802e984ef"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat{}&long={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST" :
        city1 = request.POST['city1'] 
        city2 = request.POST.get('city2', None)

        weather_data1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url)

        if city2:
            weather_data2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url)
        else:
            weather_data2 = None, None
        
        context = {
            "weather_data1": weather_data1,
            "weather_data2": weather_data2,
        }
        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")

def fetch_weather_and_forecast(city, API_KEY, current_weather_url):
    response = requests.get(current_weather_url.format(city, API_KEY)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon'] 

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 274.15, 2),
        "description": response['weather'][0]['description']   ,
        "icon": response['weather'][0]['icon'],
    }      

    # daily_forecasts = []
    # for daily_data in forecast_response['daily'][:5]:
    #     daily_forcasts.append({
    #         "day": daytime.datetime.fromtimestampe(daily_data['dt']).strfrtime("%A"),
    #         "min_temp": round(daily_data['temp']['min'] - 274.15, 2),
    #         "max_temp": round(daily_data['temp']['max'] - 274.15, 2),
    #         "description": daily_data['weather'][0]['description'],
    #         "icon": daily_data['weather'][0]['icon'],
    #     })

    return weather_data