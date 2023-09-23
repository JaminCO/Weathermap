import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c3f4bde6a02fe43dcedf6a88b0064f44'

    if request.method == 'POST':
        form = CityForm(request.POST)
        name = form.data["name"]
        cities = City.objects.filter(name=name).first()
        if cities != None:
            print("Already exists")
        else:
            form.save()

    form = CityForm()

    cities = City.objects.all()
    c_update = set()

    for city in cities:
        c_update.add(city.name)
    weather_data = []

    for city in c_update:

        r = requests.get(url.format(str(city).title())).json()
        print(r)
        
        if r["cod"] != 200:
            data = City.objects.filter(name=city).first()
            data.delete()
        else:
            city_weather = {
                'city' : str(city).title(),
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
