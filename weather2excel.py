#!/usr/bin/python

from ui_functions import *
import sys  # potrzebna do sprawdzenia, czy użytkownik podał jakiekolwiek parametry na wejściu
import argparse  # do obsługi parametrów wejściowych

# zmienne startowe
CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 54.23  # długość geograficzna
LAT = 19.23  # szerokość geograficzna
MODE = "forecast"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody
LANG = "pl"  # język do komunikacji z API, TODO zastanowić się czy ta zmienna ma być tutaj, czy w weatherApis.py?
DAYS = 5  # ilość dni do przodu na które można uzyskać prognoze pogody

print("Kontrolne wyświetlanie parametrów startowych w czystej formie")
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))
print("")

# sprawdź ilość argumentów podanych na starcie przez użytkownika
# zawsze jest minimum 1 - nazwa skryptu. Jeżeli ejst ich więcej to znaczy, ze użytkownik podał parametry startowe.
# Jeżeli tlyko 1 to znaczy, że uruchomił skrypt bez parametrów
number_of_arguments = len(sys.argv)

# jeżeli użytkownik podał jakiekolwiek argumenty to rozpocznij działanie programu na parametrach
if number_of_arguments > 1:
    parser = argparse.ArgumentParser()

    # deklaracja parametru startowego --city (nazwy miasta). nargs z wartością "*" pozwala na pobranie 1 lub więcej
    # wartości dla danego parametru - tutaj potrzebne, bo nazwy miast mogą być wielowyrazowe
    parser.add_argument("-c", "--city", nargs="*", dest="city_name", default=None,
                        help="pobiera nazwę miasta. Brak wartości domyślnej")

    # deklaracja parametru startowego --longitude (długości geograficznej)
    parser.add_argument("-lon", "--longitude", type=float, nargs="*", dest="longitude", default=None,
                        help="pobiera wartość długości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Brak wartości domyślnej.")

    # deklaracja parametru startowego --latitude (szerokości geograficznej)
    parser.add_argument("-lat", "--latitude", type=float, nargs="*", dest="latitude", default=None,
                        help="pobiera wartość szerokości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Brak wartości domyślnej.")

    # tworzy słownik argumentów
    args = parser.parse_args()

    # kontrolnie drukuje cały złownik argumentów
    print(args)

    # TODO napisać "zabezpieczenie" na wypadek gdyby użytkownik podał jednocześnie nazwę miasta oraz namiary GPS

    # jeżeli został podany parametr -c to przepisz wartość do zmiennej globalnej CITY, jak nie został podany, czyli
    # domyślnie jest None to pomiń ten krok i pozostaw niezmienioną wartość CITY
    if args.city_name is not None:
        # wyczyść nazwę miasta
        CITY = ""

        # przejdź przez całą listę wyrazów, z których może się składać nazwa miasta. Miasto mogą być 1 wyrazowe
        # np.: Gdynia, Sopot, Wejherowo, albo wielowyrazowe: Stalowa Wola, Kędzierzyn Koźle
        for word_of_city_name in args.city_name:

            # dodawaj kolejne wyrazy do zmiennej CITY (zmienna typu string)
            CITY = CITY + " " + word_of_city_name

    # pobierz wartość parematru longitude i zapisz do zmiennej globalnej LON, podanie większej ilości wartości przez
    # użytkownika będzie ignorowane - zostanie pobrana tlyko pierwsza wartość
    # TODO zmienić obsługę błędów tak aby nie przerywało skryptu gdy użytkownik poda litery
    # TODO zmienić obsługę błędów tak aby nie przerywało skryptu gdy użytkownik poda zamiast kropki przecinek (automatyczna zamiana)
    # jeżeli został podany parametr -lon to przepisz wartość do zmiennej globalnej LON, jak nie został podany, czyli
    # domyślnie jest None to pomiń ten krok i pozostaw niezmienioną wartość LON
    if args.longitude is not None:
        LON = args.longitude[0]

    # pobierz wartość parematru latitude i zapisz do zmiennej globalnej LAT, podanie większej ilości wartości przez
    # użytkownika będzie ignorowane - zostanie pobrana tlyko pierwsza wartość
    # jeżeli został podany parametr -lat to przepisz wartość do zmiennej globalnej LAT, jak nie został podany, czyli
    # domyślnie jest None to pomiń ten krok i pozostaw niezmienioną wartość LAT
    if args.latitude is not None:
        LAT = args.latitude[0]

# Jeżeli użytkownik nie podał argumentów, albo podał je błędnie to rozpocznij program od standardowego menu
#
# osobny 'if' zamiast komendy 'else' do poprzedniego 'if'a' z powodu, że gdy użytkownik źle przekaże argumenty to
# pozostaje możliwość skorzystania ze standardowego menu (wcześniejszy blok kodu ustawi number_of_arguments = 0, co
# oznacza, że coś poszło nie tak, ale użytkownik chce skorzystać z standardowego menu)
if number_of_arguments <= 1:

    # menu startowe
    print("""Weather to Excel
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

        # funckja pobiera zmienne globalne, użytkownik wprowadza miejsce, dla którego chce otrzymać informacje pogodowe
        # i funkcja zwraca wskazane miejsce ponownie do zmiennych globalnych
        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

    elif option == "2":
        MODE = "forecast"  # tryb pokazywania prognozy pogody
        print("Prognoza pogody\n")

        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

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