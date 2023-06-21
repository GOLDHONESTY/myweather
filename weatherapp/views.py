from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from datetime import datetime
from urllib.error import HTTPError


# Create your views here.

def index(request):
    now = datetime.now()
    day = now.strftime('%A')
    month = now.strftime('%B')
    year = now.strftime('%Y')

    if request.method == 'POST':
        API_key = '0dffbe8a5fac977fe8fdc3000ffebff3'
        city = request.POST['searchcity']
        messa = 'invalid city name pls try again'
        data1 = {
            
            'day': day,
            'month': month,
            'year': year,
            'message':messa
        }
        encoded_city = urllib.parse.quote(city)
        try:
            source = urllib.request.urlopen(f'https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&appid={API_key}').read()
            list_of_data = json.loads(source)

        except HTTPError as e:
            if e.code == 404:
                return render(request, 'index.html', data1)
            elif UnboundLocalError:
                return render(request, 'index.html', data1)
        else:  

            currentdata = {
                'country_code': str(list_of_data['sys']['country']),
                'temp': str(round(list_of_data['main']['temp'])),
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'icon': str(list_of_data['weather'][0]['icon']),
                'lon': list_of_data['coord']['lon'],
                'lat':  list_of_data['coord']['lat'],

                'city': city,
                'day': now.strftime('%A'),
                'month':now.strftime('%B'),
                'year': now.strftime('%Y'),
                
            }

            lon = currentdata['lon']
            lat = currentdata['lat']

        

            source2 = urllib.request.urlopen(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}').read()

            lists_of_data2 = json.loads(source2)

            forecasts_data = []
            previous_date = ''

            for data in lists_of_data2['list']:
                date = data['dt_txt'].split(' ')[0]
                if date != previous_date:
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    day_of_week = date_obj.strftime('%A')
                    forecast = {
                        'date': day_of_week,
                        'temperature': str(round(data['main']['temp']-273.15)),
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                    }
                    forecasts_data.append(forecast)
                    previous_date = date

            context = {
                'currentdata': currentdata,
                'forecasts_data': forecasts_data[1:],
            }


        return render(request, 'index.html', context)
    else:
        
        data2 = {
            
            'day': day,
            'month': month,
            'year': year,
            
        }
        return render(request, 'index.html', data2)