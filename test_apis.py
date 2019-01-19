# plik w którym znajdują się elementy na których można testować działanie API pogodowych

#!/usr/bin/python
import os
import sys

import csv
import json # only for development
import statistics

from weatherApis import *
from geocoder import *

CITY = "SOPOT"  # nazwy miast z małych liter aby łatwiej było operać na API
COUNTRY = ""

geocoder = geocoder()
num_results = geocoder .getQueryResults(CITY, COUNTRY)
if num_results>1:
    geocoder.listResults()
    choice = ""
    while not isinstance(choice, int) or choice<0 or choice>num_results-1:
        option = input("Wybierz numer z właściwym miejscem i naciśnij ENTER: ")
        try:
          choice = int(option)-1
        except:
          print("Nie wprowadzono prawidłowej wartości z przedziału <1;"+num_results+">")
elif num_results == 1:
    choice = 0
else:
    print("Nie udało się wyznaczyć współrzednych dla podanej frazy wyszukiwania.")
    print("Proszę spróbować wyszukiwania dla innej frazy lub za pomocą współrzednych geograficznych.")
    quit()

coord = geocoder.getCoordindates(choice)
if coord is False:
    print("Nie udało się uzyskać współrzędnych wybranej miejscowości.")
    print("Proszę spróbować wyszukiwania dla innej frazy lub za pomocą współrzednych geograficznych.")
    quit()

LAT = coord["lat"]
LON = coord["lon"]

print("\nWyszukiwanie dla: "+geocoder.RESULT_LIST[choice]["display_name"]+"\n(DŁUG,SZER) = ("+LAT+","+LON+")")
#quit()

# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
#LON = 18.5318800  # długość geograficzna
#LAT = 54.5188900  # szerokość geograficzna
MODE = "current"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 1  # ilość dni do przodu na które można uzyskać prognoze pogody
SILENT = False #  false - print to console information during request to API

weatherDataset = []

#APIS = ["OpenWeather.csv"]


# check API keys to determine if the weather can be obtained(includning timezones)
if( check_API_keys(verify_online=False)==0 ):
  sys.exit("Nie skonfigurowano żadnego systemu do pobierania danych o pogodzie.\n Program nie może działać.\n Wpisz xxx -help, aby dowiedzieć się, jak dokonać konfiguracji.")


"""for API in os.listdir("config/API/"):"""
for API in APIS:
  if API.endswith(".csv"):
    wa = WeatherApis()
    if wa.read_conf(API) == False:
      continue
    if wa.get_weather(MODE, LANG, DAYS, SILENT, LAT, LON):
      weatherDataset.append( wa.parse_result(MODE, DAYS) )
    else:
      print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search)

CSV="api_name,"
for factor in factors:
    if(MODE=="forecast" and len(factorsDict[factor].type)==2 ) or (MODE=="current" and len(factorsDict[factor].type)==1):
        CSV = CSV +factor+","
CSV=CSV+"\r\n"

def is_number(str):
    try:
        float(str)
        return True
    except:
        return False

for day in range(0,DAYS):
    STAT = {}
    for factor in factors:
        STAT[factor]=[]
    for wynikiAPI in weatherDataset:
        CSV = CSV + "\"" + str(wynikiAPI[day]["api_name"]) + "\","
        for factor in wynikiAPI[day]:
            if(MODE=="forecast" and len(factorsDict[factor].type)==2 ) or (MODE=="current" and len(factorsDict[factor].type)==1):
                CSV = CSV + "\"" + str(wynikiAPI[day][factor]) + "\","
                if( is_number(wynikiAPI[day][factor]) ):
                    STAT[factor].append( float(wynikiAPI[day][factor]) )
        CSV=CSV+"\r\n"
    CSV=CSV+"MEAN ± SD:,"
    #calculating statistics
    for factor in factors:
        if(MODE=="forecast" and len(factorsDict[factor].type)==2 ) or (MODE=="current" and len(factorsDict[factor].type)==1):
            if len(STAT[factor])>0:
                #STAT[factor+"_mean"] = round(statistics.pstdev(STAT[factor]),1)
                #STAT[factor+"_mean"] = round(statistics.pstdev(STAT[factor]),1)
                CSV=CSV+"\""+str( round(statistics.mean(STAT[factor]),1))+"±"+str( round(statistics.pstdev(STAT[factor]),1) )+"\","
            else:
                CSV=CSV+"\"\","

    CSV=CSV+"\r\n\r\n"




f = open( 'wyniki.csv', 'w' )
f.write( CSV )
f.close()


with open('data.json', 'w') as outfile:
    for WD in weatherDataset:
        json.dump(WD, outfile)
        #print(json.dumps(WD, sort_keys=False, indent=4))

