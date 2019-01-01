#!/usr/bin/python
from weatherApis import *
#from Factors import *
import csv
import json # only for development

weatherDataset=[]

#TODO for loop all  .csv files from /config// directory
APIS=["APIXU.csv","OpenWeather.csv","WAQI.csv","Weatherbit.csv","DarkSky.csv"]
#APIS=["APIXU.csv"]

for API in APIS:
  wa = WeatherApis()
  wa.read_conf(API)
  #wa.print_api_verification()
  if wa.get_weather("Gdynia"):
    weatherDataset.append( wa.parse_result() )
  else:
    print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search_city)

for WD in weatherDataset:
  print(json.dumps(WD, sort_keys=False, indent=4))
#print(WeatherDataset)

#CURRENT  (5 serwisów)
#http://api.apixu.com/v1/current.json?key=c953a701381744908f8162100182912&q=Gdynia
#https://api.darksky.net/forecast/652e2a9ecce5d60cded939c25af6cf05/54.51889,18.53188?units=si&exclude=minutely,hourly
#http://api.openweathermap.org/data/2.5/weather?q=Gdynia&units=metric&APPID=65359e9517b2c3eb514ddd698ad3c8ee
#https://api.weatherbit.io/v2.0/current?city=Gdynia&key=5be1f8746a68417c8b7d9ce28603ff14
#http://api.waqi.info/feed/New%20York/?token=c74908ddf2f7d5bbe6886de8115f70683779ce1e

#FORECAST DAYS (4 serwisy)
#http://api.apixu.com/v1/forecast.json?key=c953a701381744908f8162100182912&q=Gdynia&days=10
#https://api.darksky.net/forecast/652e2a9ecce5d60cded939c25af6cf05/54.51889,18.53188?units=si&exclude=minutely,hourly
#http://api.openweathermap.org/data/2.5/forecast?q=Gdynia&units=metric&APPID=65359e9517b2c3eb514ddd698ad3c8ee
#https://api.weatherbit.io/v2.0/forecast/daily?city=Gdynia&key=5be1f8746a68417c8b7d9ce28603ff14
