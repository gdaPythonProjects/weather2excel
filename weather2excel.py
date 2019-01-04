#!/usr/bin/python

from ui_functions import *

CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 54.23  # długość geograficzna
LAT = 19.23  # szerokość geograficzna
MODE = "forecast"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 5  # ilość dni do przodu na które można uzyskać prognoze pogody

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

# kontrolny wydruk zmiennych podanych przez użytkownika
print("")
print("Kontrolny wydruk zmiennych")
print("CITY: ", CITY)
print("LON: ", LON)
print("LAT: ", LAT)