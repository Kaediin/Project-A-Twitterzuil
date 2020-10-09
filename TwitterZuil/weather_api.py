import urllib.request
import json
from TwitterZuil.models import *

def getWeather(city):
    try:
        url = "http://api.weatherapi.com/v1/current.json?key=59fb3462ec5449cbb4a121545200810&q={}".format(city)
        response = urllib.request.urlopen(url).read()
        json_obj = str(response, 'utf-8')
        data = json.loads(json_obj)
        weer = Weer(
            data['current']['condition']['text'],
            data['current']['temp_c'],
            data['current']['condition']['icon'],
            data['current']['wind_dir'],
            data['current']['wind_kph'],
            data['current']['precip_mm'],
            data['current']['feelslike_c'],
            data['current']['uv'],
            data['location']['region'],
        )

        return weer
    except OSError:
        print('Error fetching data from API')
        return None

def isValidCity(city):
    weer = getWeather(city)
    return weer
