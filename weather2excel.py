#!/usr/bin/python
from weatherApis import *
# from Factors import *
import csv
import json # only for development


CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 54.23  # długość geograficzna
LAT = 19.23  # szerokość geograficzna
MODE = "forecast"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 5  # ilość dni do przodu na które można uzyskać prognoze pogody



# funkcja pobierająca dane o miejscu od użytkownika i zmieniająca odpowiednie zmienne dla API pogodowych
# funkcja ta zmienia następujące zmienne globalne: CITY, LON, LAT
def get_place_from_user():
    print("""
    W jaki sposób chcesz wskazać miejsce?
      1. Podam nazwę miejscowości.
      2. Podam współrzędne GPS.
    """)

    # zeruję wartość zmiennej option, aby móc ją ponownie wykorzystać
    option = ""

    # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
    while option != "1" and option != "2":
        option = input("Wprowadź numer opcji (1/2) i naciśnij ENTER: ")

        # sprawdź czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
        if option != "1" and option != "2":
            print("\nNie ma takiej opcji! Spróbuj jeszcze raz...\n")

    if option == "1":
        global CITY  # daję znać, że mam zapisywać wartość do zmiennej globalnej (z poza funkcji)
        CITY = input("\nPodaj miasto: ").lower()  # małe litery dla ułatwienia komunikacji z API

    elif option == "2":

        # pobieram dane dla długości geograficznej, oczekuję liczby w zakresie od 0 do 180

        global LON  # korzystaj ze zmiennej globalnej

        # ustaw wartość poza zakres poniższej pętli, aby mogła wykonać się przynajmenij 1 raz
        # w innym wypadku pobrałby wartość zdefiniowaną na początku programu, gdzie wartość jest prawidłowa
        # i spowodowałoby to nie wykonanie się pętli
        LON = 1000

        isCorrectRange = 0  # flaga określająca, czy podana przez użytkownika wartość mieści się w zakresie (tutaj 0-180)

        while isCorrectRange != 1:
            isCorrectValue = 0  # flaga informująca czy użytkownik prawidłowo wprowadził dane

            while isCorrectValue != 1:  # wykonuje pętlę póki nie będzie podana prawidłowa wartość liczbowa

                try:  # wypróbuj blok kodu
                    tmp_lon = input("Podaj długość geograficzną (w formie ułamka dziesiętnego od 0 do 180): ")

                    # jeżeli użytkownik użył przecinka do oddzielenia części całości od ułamkowej to zamień go na kropkę
                    if "," in tmp_lon:
                        tmp_lon = tmp_lon.replace(",", ".")

                    # konwertuj do typu float i zapisz do zmiennej globalnej LON
                    LON = float(tmp_lon)

                except ValueError:  # oczekuj błędu niepoprawnych danych, jeżeli wystąpi to wyświetl komunikat
                    print("Nieprawidłowy format współrzędnej! Pamiętaj, że ma być liczbą dziesiętną!\n")

                else:  # jeżeli pójdzie dobrze oznacz correcValue na 1 jako prawidłowy
                    isCorrectValue = 1

            # sprawdź czy wartość jest w prawidłowym zakresie
            if 0 < LON < 180:
                isCorrectRange = 1
            else:
                print("Wartość poza zakresem! Spróbuj jeszcze raz!")

        # jeżeli użytkownik podał równe 180 stopni zamieniam je na 0, aby poprawnie wprowadzić współrzędne do API
        # nie każde API może prawidłowo przyjąć wartość 180 i większą
        if LON == 180:
            LON = 0

        # koniec pobierania długości geograficznej
    
        # pobieram wartość szerokości geograficznej. Oczekuję wartości od 0 do 90
        # wyjaśnienie działania identyczne jak wyżej dla długości geograficznej

        global LAT
        LAT = 1000

        isCorrectRange = 0  # resetuję flagę

        while isCorrectRange != 1:
            isCorrectValue = 0  # resetuję flagę

            while isCorrectValue != 1:

                try:
                    tmp_lat = input("Podaj szerokość geograficzną (w formie ułamka dziesiętnego od 0 do 90): ")

                    if "," in tmp_lat:
                        tmp_lat = tmp_lat.replace(",", ".")

                    LAT = float(tmp_lat)

                except ValueError:
                    print("Nieprawidłowy format współrzędnej! Pamiętaj, że ma być liczbą dziesiętną!\n")

                else:
                    isCorrectValue = 1

            if 0 < LAT < 90:
                isCorrectRange = 1
            else:
                print("Wartość poza zakresem! Spróbuj jeszcze raz!")

        # poprawiam wartość graniczną dla szerokości geograficznej
        if LAT == 90:
            LAT = 0

        # koniec pobierania szerokości geograficznej

# koniec funkcji get_place_from_user()


# menu startowe
print("""
---------------------------------------------------------
Weather to Excel
Tutaj możesz sprawdzić aktualną pogodę dla danego miejsca oraz aktualne zanieczysczenie powietrza, albo sprawdzić prognozę pogody.

Co chcesz zrobić?
  1. Pokaz aktualne dane.
  2. Pokaż prognozę pogody.
  3. Ostatnio wyszukiwane.
""")

option = ""  # zmienna określająca, którą opcję wybrał uzytkownik

# wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
while option != "1" and option != "2" and option != "3":
    # użytkownik pworwadza numer komendy - numer jest w postaci string, aby uniknąć błędów związanych z podaniem
    # nieprawdiłowego znaku lub ciągu znaków
    option = input("Wprowadź numer opcji (1/2/3) i naciśnij ENTER: ")

    # sprawdź czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
    if option != "1" and option != "2" and option != "3":
        print("\nNie ma takiej opcji! Spróbuj jeszcze raz...\n")

# dalej zbieram potrzebne informacje do wyświetlenia danych
if option == "1":
    MODE = "current"  # tryb pokazywania aktualnych danych
    print("Aktualne dane\n")

    get_place_from_user()

elif option == "2":
    MODE = "forecast"  # tryb pokazywania prognozy pogody
    print("Prognoza pogody\n")

    get_place_from_user()

elif option == "3":
    print("Ostatnio wyszukiwane\n")
    # TODO wykonać funkcję pobierania infromacji o ostatnim wyszukiwaniu

else:
    print("Coś poszło nie tak przy wybieraniu opcji!")

# kontrolny wydruk zmiennych
# print("")
# print(CITY)
# print(LON)
# print(LAT)

weatherDataset = []

# TODO for loop all  .csv files from /config// directory
APIS = ["APIXU.csv", "OpenWeather.csv", "WAQI.csv", "Weatherbit.csv", "DarkSky.csv","Climacell.csv"]

#APIS = ["Climacell.csv"]

for API in APIS:
  wa = WeatherApis()
  wa.read_conf(API)   #wa.print_config()
  #wa.print_api_verification()
  if wa.get_weather(MODE, LANG, DAYS, LON,LAT):
    weatherDataset.append( wa.parse_result(MODE, DAYS) )
  else:
    print("Problem z uzyskaniem danych z "+wa.config["api_name"]+". Adres: "+wa.url_search)

with open('data.json', 'w') as outfile:
    for WD in weatherDataset:
        json.dump(WD, outfile)
        print(json.dumps(WD, sort_keys=False, indent=4))

# print(WeatherDataset)