# plik w którym znajdują się elementy na których można testować działanie API pogodowych

#!/usr/bin/python

from weatherApis import *
# from Factors import *
import csv
import json # only for development
import os

CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 19.940984  # długość geograficzna
LAT = 50.062006  # szerokość geograficzna
MODE = "current"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 5  # ilość dni do przodu na które można uzyskać prognoze pogody

weatherDataset = []

# TODO for loop all  .csv files from /config// directory
#APIS = ["APIXU.csv", "OpenWeather.csv", "WAQI.csv", "Weatherbit.csv", "DarkSky.csv", "Climacell.csv","Airly.csv"]

APIS = ["Airvisual.csv","APIXU.csv"]


"""for API in os.listdir("config/API/"):"""
for API in APIS:
  if API.endswith(".csv"):
    wa = WeatherApis()
    if wa.read_conf(API) == False:
      continue
    if wa.get_weather(MODE, LANG, DAYS, LON,LAT):
      weatherDataset.append( wa.parse_result(MODE, DAYS) )
    else:
      print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search)


with open('data.json', 'w') as outfile:
    for WD in weatherDataset:
        json.dump(WD, outfile)
        print(json.dumps(WD, sort_keys=False, indent=4))
