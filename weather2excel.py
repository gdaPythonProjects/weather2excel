#!/usr/bin/python
from weatherApis import *
#from Factors import *
import csv
import json # only for development

CITY="Gdynia"
#MODE="current"
MODE="forecast"
LANG="pl"
DAYS=5

weatherDataset=[]

#TODO for loop all  .csv files from /config// directory
APIS=["APIXU.csv","OpenWeather.csv","WAQI.csv","Weatherbit.csv","DarkSky.csv"]
#APIS=["OpenWeather.csv"]

for API in APIS:
  wa = WeatherApis()
  wa.read_conf(API)   #wa.print_config()
  #wa.print_api_verification()
  if wa.get_weather(MODE, LANG, DAYS, CITY):
    weatherDataset.append( wa.parse_result(MODE, DAYS) )
  else:
    print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search)

with open('data.json', 'w') as outfile:
  for WD in weatherDataset:
    json.dump(WD, outfile)
    print(json.dumps(WD, sort_keys=False, indent=4))
#print(WeatherDataset)


