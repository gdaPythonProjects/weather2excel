#!/usr/bin/python

# region import
from ui_functions import *
import sys  # potrzebna do sprawdzenia, czy użytkownik podał jakiekolwiek parametry na wejściu
import argparse  # do obsługi parametrów wejściowych
import geocoder
# endregion

# region zmienne startowe
CITY = "gdynia"  # nazwy miast z małych liter aby łatwiej było operać na API
# współrzedne dla Gdyni pobrane z portalu https://www.wspolrzedne-gps.pl/
LON = 54.5142351  # długość geograficzna
LAT = 18.5358849  # szerokość geograficzna

MODE = "current"  # "current" podaję aktualne dane, alternatywny tryb -> "forecast" - prognoza, ale tylko dla pogody

LANG = "pl"  # język do komunikacji z API
DAYS = 5  # ilość dni do przodu na które można uzyskać prognoze pogody

option = None  # zmienna określająca, którą opcję wybrał uzytkownik
error_in_start_parameters = 0  # zmienna określająca czy wszystkie parametry zostały podane poprawnie przez Użytkownika
# endregion

# wyświetl wiadomość powitalną
welcome_message()

# sprawdź ilość argumentów podanych na starcie przez użytkownika
#  zawsze jest minimum 1 - nazwa skryptu. Jeżeli ejst ich więcej to znaczy, ze użytkownik podał parametry startowe.
#  Jeżeli tylko 1 to znaczy, że uruchomił skrypt bez parametrów
number_of_arguments = len(sys.argv)

# jeżeli użytkownik podał jakiekolwiek argumenty to rozpocznij działanie programu na parametrach

# region parametry startowe przechwytywanie i wstępna obsługa
if number_of_arguments > 1:

    # region przechwytywanie parametrów
    parser = argparse.ArgumentParser()

    # deklaracja parametru startowego --city (nazwy miasta). nargs z wartością "*" pozwala na pobranie 1 lub więcej
    # wartości dla danego parametru - tutaj potrzebne, bo nazwy miast mogą być wielowyrazowe
    # wartość domyślna zapisana w zmiennych globalnych na początku programu zamiast tutaj w parserze, aby uniknąć
    #  późniejszych problemów
    parser.add_argument("-c", "--city", nargs="*", dest="city", default=None,
                        help="pobiera nazwę miasta. Wartość domyślna: Gdynia")

    # deklaracja parametru startowego --longitude (długości geograficznej)
    # wartość domyślna (54.23) zapisana w zmiennych globalnych na początku programu zamiast tutaj w parserze, aby
    #  uniknąć późniejszych problemów
    parser.add_argument("-lon", "--longitude", nargs="*", dest="longitude", default=None,
                        help="pobiera wartość długości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Wartość domyślna: 54.23 (dla Gdyni).")

    # deklaracja parametru startowego --latitude (szerokości geograficznej)
    # wartość domyślna zapisana w zmiennych globalnych to 19.23
    parser.add_argument("-lat", "--latitude", nargs="*", dest="latitude", default=None,
                        help="pobiera wartość szerokości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Wartość domyślna: 19.23 (dla Gdyni).")

    # parametr decydujące, czy program ma działać w trybie "current", czy "forecast"
    parser.add_argument("-m", "--mode", dest="mode", choices=['current', 'forecast'], default=None,
                        help="ustawia tryb działania programu - 'current' pokazuje aktualne dane,"
                             "'forecast' pokazuje prognozę (tylko dla pogody!)")

    # tworzy słownik argumentów
    args = parser.parse_args()
    # endregion

# region gdy użytkownik spróbował jednocześnie podać nazwę miasta oraz namiary GPS w parametrach startpwych...
    if (args.city is not None) and ((args.longitude is not None) or (args.latitude is not None)):
        print("""
OSTRZEZENIE! Podjęto próbę jednoczesnego podania: nazwy miasta i współrzędnych GPS!

Co chcesz zrobić?
    1. Skorzystać z podanej nazwy miejscowości.
    2. Skorzystać z podanych współrzędnych GPS.
    3. Przejść do menu startowego.
    4. Zakończyć działanie programu.
""")

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
        while option is None:

            # użytkownik wporwadza numer komendy - numer jest w postaci string, aby uniknąć błędów związanych z podaniem
            #  nieprawdiłowego znaku lub ciągu znaków
            option = check_user_choice_is_correct(input("Wprowadź numer opcji (1/2/3/4) i naciśnij ENTER: "),
                                                  ["1", "2", "3", "4"])
            print("")  # nowa linia dla poprawy czytelności

            # jeżeli nie została zwrócona żadna opcja to znaczy, że użytkownik podał, opcję spoza dopuszczonych
            if option is None:
                print("Nie ma takiej opcji! Spróbuj jeszcze raz...\n")

        # reaguj na prawidłowo wybraną opcję
        if option == "1":
            # wyzeruj zmienne -lon i -lat
            args.longitude = None
            args.latitude = None

        elif option == "2":
            # wyczyść nazwę miasta
            args.city = None

        elif option == "3":
            # ustawienie number_of_arguments na 0 spowoduje wywołanie menu start w dalszej części programu poprzez
            #  zasymulowanie jakby argumenty nie zostały podane (powinno być 1, ale podanie wartości 0 zasugeruje, że
            #  to jest sztucznie wytworzona zmiana)
            number_of_arguments = 0

            # wyczyść wszystkie dane podane w parametrach przez użytkownika
            args.city = None
            args.longitude = None
            args.latitude = None

        elif option == "4":
            print("Zakończono działanie programu.")
            exit()

        else:
            print("Coś poszło nie tak!")
            exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma
# endregion

# region został wywołany parametr -city
    #  to przepisz jego wartość do zmiennej globalnej CITY, a jak nie została podana nowa wartość dla niego (domyślnie
    #  w parserze argumentów startowych jest None) to pomiń ten krok i pozostaw niezmienioną wartość CITY (zgodną
    #  z wartością domyslną podaną dla zmiennych globalnych na poczatku)
    if (args.city is not None) and (args.longitude is None) and (args.latitude is None):
        # wyczyść nazwę miasta
        CITY = ""

        # przejdź przez całą listę wyrazów, z których może się składać nazwa miasta. Miasto mogą być 1 wyrazowe
        #  np.: Gdynia, Sopot, Wejherowo, albo wielowyrazowe: Stalowa Wola, Kędzierzyn Koźle
        for word_of_city_name in args.city:

            # dodawaj kolejne wyrazy do zmiennej CITY (zmienna typu string)
            CITY = CITY + word_of_city_name + " " 

        # oczyszczanie zmiennej z białych znaków na początku i na końcu
        CITY = CITY.strip()

        LON, LAT = get_coords_by_city_name(CITY, "")

        error_in_start_parameters = 0
# endregion

# region jeżeli zostały wywołane parametry -lon i -lat
    #  to pobierz dane z tych parametrów i przekaż je do zmiennych globlanych LON i LAT. Podanie przez użytkownika
    #  większej ilości liczb dla danego parametru (np.: -lon 34.5 78 43.2) będzie zignorowane i zostanie pobrana tylko
    #  pierwsza wartość (tu w przykładzie 34.5)
    elif (args.city is None) and (args.longitude is not None) and (args.latitude is not None):

        # sprawdzam, czy wartości podane przez użytkownika z pomocą parametrów są prawidłowe
        is_correct_value_LON, is_correct_range_LON, LON = check_GPS_value_from_user(args.longitude[0], 0, 180)
        is_correct_value_LAT, is_correct_range_LAT, LAT = check_GPS_value_from_user(args.latitude[0], 0, 90)

        # jeżeli wszystko jest ok to ustawiam flagę error_in_start_parameters na 0
        if (is_correct_value_LON == 1 and
                is_correct_range_LON == 1 and
                is_correct_value_LAT == 1 and
                is_correct_range_LAT == 1):

            error_in_start_parameters = 0

            # pobierz miejsce na podstawie koordynatów GPS
            g = geocoder.geocoder()
            place = g.getQueryReverseResults(LAT, LON)

            # jeżeli nie nie zwróciło żadnego miasta
            if place['city'] == '':
                CITY = 'Brak miasta w tym miejscu'
            else:
                CITY = place['city']

        # jeżeli jest jakikolwiek błąd przy sprawdzaniu poprawności to ustawiam error_in_start_parameters na 1
        else:
            error_in_start_parameters = 1

    else:
        error_in_start_parameters = 1
# endregion

# region jeżeli został wywołany parametr --mode
    if args.mode is not None:
        MODE = args.mode
# endregion

# region obsługa błędnie podanych parametrów

    # wyświetl info o błędzie we współrzędnych wtedy gdy taki błąd znajdziesz oraz gdy użytkownik rzeczywiście
    #  podał jakikolwiek argument
    if error_in_start_parameters == 1 and number_of_arguments > 1:
        print("""
BŁĄD! Podana tylko jedna współrzędna GPS lub współrzędne podane niepoprawnie (wartość nieliczbowa bądź poza zakresem).

Co chcesz zrobić?
    1. Przejść do menu startowego.
    2. Zakończyć działanie programu.
""")

        # zerowanie
        option = None

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
        while option is None:
            option = check_user_choice_is_correct(input("Wprowadź numer opcji (1/2) i naciśnij ENTER: "), ["1", "2"])
            print("")  # nowa linia dla poprawy czytelności

            # sprawdź, czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
            if option is None:
                print("Nie ma takiej opcji! Spróbuj jeszcze raz...\n")

        # reaguj na prawidłowo wybraną opcję
        if option == "1":
            # ustawienie number_of_arguments na 0 spowoduje wywołanie menu start w dalszej części programu poprzez
            #  zasymulowanie jakby argumenty nie zostały podane (powinno być 1, ale podanie wartości 0 zasugeruje, że
            #  to jest sztucznie wytworzona zmiana)
            number_of_arguments = 0

            # wyczyść wszystkie dane podane w parametrach przez użytkownika
            args.city = None
            args.longitude = None
            args.latitude = None

        elif option == "2":
            print("Zakończono działanie programu")
            exit()

        else:
            print("Coś poszło nie tak!")
            exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma
# endregion

# region menu startowe
# Jeżeli użytkownik nie podał argumentów, albo podał je błędnie number_of_arguments == 0) to rozpocznij program od
#  menu startowego
if number_of_arguments <= 1:

    # menu startowe
    print("""    
Co chcesz zrobić?
  1. Pokaz aktualne dane.
  2. Pokaż prognozę pogody.
  3. Zakończ działanie programu.
""")

    option = None  # resetuję zmienną

    # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
    while option is None:
        option = check_user_choice_is_correct(input("Wprowadź numer opcji (1/2/3) i naciśnij ENTER: "),
                                              ["1", "2", "3"])
        print("")  # nowa linia dla poprawy czytelności

        # sprawdź czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
        if option is None:
            print("Nie ma takiej opcji! Spróbuj jeszcze raz...\n")

    # dalej zbieram potrzebne informacje do wyświetlenia danych
    if option == "1":
        MODE = "current"  # tryb pokazywania aktualnych danych
        print("Aktualne dane")

        # funkcja pobiera zmienne globalne, użytkownik wprowadza miejsce, dla którego chce otrzymać informacje pogodowe
        #  i funkcja zwraca wskazane miejsce ponownie do zmiennych globalnych
        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

    elif option == "2":
        MODE = "forecast"  # tryb pokazywania prognozy pogody
        print("Prognoza pogody")

        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

    elif option == "3":
        print("Zakończono działanie programu.")
        exit()

    else:
        print("Coś poszło nie tak przy wybieraniu opcji!")
        exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma
# endregion

# region kontrolny wydruk zmiennych podanych przez użytkownika
print("")
print("Kontrolny wydruk zmiennych")
print("CITY: ", CITY)
print("LON: ", LON)
print("LAT: ", LAT)
print("MODE: ", MODE)
# endregion
