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
# Jeżeli tylko 1 to znaczy, że uruchomił skrypt bez parametrów
number_of_arguments = len(sys.argv)

option = ""  # zmienna określająca, którą opcję wybrał uzytkownik

# jeżeli użytkownik podał jakiekolwiek argumenty to rozpocznij działanie programu na parametrach
if number_of_arguments > 1:
    parser = argparse.ArgumentParser()

    # deklaracja parametru startowego --city (nazwy miasta). nargs z wartością "*" pozwala na pobranie 1 lub więcej
    # wartości dla danego parametru - tutaj potrzebne, bo nazwy miast mogą być wielowyrazowe
    # wartość domyślna zapisana w zmiennych globalnych na początku programu zamiast tutaj w parserze, aby uniknąć
    #  późniejszych problemów
    parser.add_argument("-c", "--city", nargs="*", dest="city_name", default=None,
                        help="pobiera nazwę miasta. Wartość domyślna: Gdynia")

    # deklaracja parametru startowego --longitude (długości geograficznej)
    # wartość domyślna zapisana w zmiennych globalnych na początku programu zamiast tutaj w parserze, aby uniknąć
    #  późniejszych problemów
    parser.add_argument("-lon", "--longitude", nargs="*", dest="longitude", default=None,
                        help="pobiera wartość długości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Wartość domyślna: 54.23 (dla Gdyni).")

    # deklaracja parametru startowego --latitude (szerokości geograficznej)
    # wartość domyślna zapisana w zmiennych globalnych na początku programu zamiast tutaj w parserze, aby uniknąć
    #  późniejszych problemów
    parser.add_argument("-lat", "--latitude", nargs="*", dest="latitude", default=None,
                        help="pobiera wartość szerokości geograficznej w formie liczby całkowitej lub ułamka "
                             "dziesiętnego. Pamiętaj, że część całości od ułamka oddziela '.' (KROPKA) ! "
                             "Wartość domyślna: 19.23 (dla Gdyni).")

    # tworzy słownik argumentów
    args = parser.parse_args()

    # kontrolnie drukuje cały złownik argumentów
    print(args)

    # zmienna określająca czy pwszystkie parametry zostały podane poprawnie przez Użytkownika
    error_in_start_parameters = 0

    # "zabezpieczenie" na wypadek gdyby użytkownik spróbował podać jednocześnie nazwę miasta oraz namiary GPS
    if (args.city_name is not None) and ((args.longitude is not None) or (args.latitude is not None)):
        print("""
OSTRZEZENIE! Podjęto próbę jednoczesnego podania: nazwy miasta i współrzędnych GPS!

Co chcesz zrobić?
    1. Skorzystać z podanej nazwy miejscowości.
    2. Skorzystać z podanych współrzędnych GPS.
    3. Przejść do menu startowego.
    4. Zakończyć działanie programu.
""")

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
        while option != "1" and option != "2" and option != "3" and option != "4":
            # użytkownik wporwadza numer komendy - numer jest w postaci string, aby uniknąć błędów związanych z podaniem
            #  nieprawdiłowego znaku lub ciągu znaków
            option = input("Wprowadź numer opcji (1/2/3/4) i naciśnij ENTER: ")
            print("")  # nowa linia dla poprawy czytelności

            # sprawdź, czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
            if option != "1" and option != "2" and option != "3" and option != "4":
                print("Nie ma takiej opcji! Spróbuj jeszcze raz...\n")

        # reaguj na prawidłowo wybraną opcję
        if option == "1":
            # wyzeruj zmienne -lon i -lat
            args.longitude = None
            args.latitude = None

        elif option == "2":
            # wyczyść nazwę miasta
            args.city_name = None

        elif option == "3":
            # ustawienie number_of_arguments na 0 spowoduje wywołanie menu start w dalszej części programu poprzez
            #  zasymulowanie jakby argumenty nie zostały podane (powinno być 1, ale podanie wartości 0 zasugeruje, że
            #  to jest sztucznie wytworzona zmiana)
            number_of_arguments = 0

            # wyczyść wszystkie dane podane w parametrach przez użytkownika
            args.city_name = None
            args.longitude = None
            args.latitude = None

        elif option == "4":
            print("Zakończono działanie programu.")
            exit()

        else:
            print("Coś poszło nie tak!")
            exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma

    # jeżeli został podany parametr -c oraz użytkownik nie podał parametrów -lon i -lat
    #  to przepisz wartość do zmiennej globalnej CITY, a jak nie została podana nowa wartość dla niego (domyślnie
    #  w parserze argumentów startowych jest None) to pomiń ten krok i pozostaw niezmienioną wartość CITY (zgodną
    #  z wartością domyslną podaną dla zmiennych globalnych na poczatku)
    if (args.city_name is not None) and (args.longitude is None) and (args.latitude is None):
        # wyczyść nazwę miasta
        CITY = ""

        # przejdź przez całą listę wyrazów, z których może się składać nazwa miasta. Miasto mogą być 1 wyrazowe
        #  np.: Gdynia, Sopot, Wejherowo, albo wielowyrazowe: Stalowa Wola, Kędzierzyn Koźle
        for word_of_city_name in args.city_name:

            # dodawaj kolejne wyrazy do zmiennej CITY (zmienna typu string)
            CITY = CITY + " " + word_of_city_name

        error_in_start_parameters = 0

    # jeżeli zostały podane parametry -lon i -lat, ale nie został podany -city to pobierz dane z tych parametrów
    #  i przekaż je do zmiennych globlanych LON i LAT. Podanie przez użytkownika większej ilości liczb dla danego
    #  parametru (np.: -lon 34.5 78 43.2) będzie zignorowane i zostanie pobrana tylko pierwsza wartość
    #  (tu w przykładzie 34.5)
    elif (args.city_name is None) and (args.longitude is not None) and (args.latitude is not None):

        # sprawdzam, czy wartości podane przez użytkownika z pomocą parametrów są prawidłowe
        is_correct_value_LON, is_correct_range_LON, LON = check_GPS_value_from_user(args.longitude[0], 0, 180)
        print("Dla LON: ", is_correct_value_LON, is_correct_range_LON, LON)
        is_correct_value_LAT, is_correct_range_LAT, LAT = check_GPS_value_from_user(args.latitude[0], 0, 90)
        print("Dla LAT: ", is_correct_value_LAT, is_correct_range_LAT, LAT)

        # jeżeli wszystko jest ok to ustawiam flagę error_in_start_parameters na 0
        if (is_correct_value_LON == 1 and
                is_correct_range_LON == 1 and
                is_correct_value_LAT == 1 and
                is_correct_range_LAT == 1):

            error_in_start_parameters = 0

        # jeżeli jest jakikolwiek błąd przy sprawdzaniu poprawności to ustawiam error_in_start_parameters na 1
        else:
            error_in_start_parameters = 1

    else:
        error_in_start_parameters = 1

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
        option = 0

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
        while option != "1" and option != "2":
            # użytkownik wporwadza numer komendy - numer jest w postaci string, aby uniknąć błędów związanych z podaniem
            #  nieprawdiłowego znaku lub ciągu znaków
            option = input("Wprowadź numer opcji (1/2) i naciśnij ENTER: ")
            print("")  # nowa linia dla poprawy czytelności

            # sprawdź, czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
            if option != "1" and option != "2":
                print("Nie ma takiej opcji! Spróbuj jeszcze raz...\n")

        # reaguj na prawidłowo wybraną opcję
        if option == "1":
            # ustawienie number_of_arguments na 0 spowoduje wywołanie menu start w dalszej części programu poprzez
            #  zasymulowanie jakby argumenty nie zostały podane (powinno być 1, ale podanie wartości 0 zasugeruje, że
            #  to jest sztucznie wytworzona zmiana)
            number_of_arguments = 0

            # wyczyść wszystkie dane podane w parametrach przez użytkownika
            args.city_name = None
            args.longitude = None
            args.latitude = None

        elif option == "2":
            print("Zakończono działanie programu")
            exit()

        else:
            print("Coś poszło nie tak!")
            exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma
    # koniec reakcji na błędy w parametrach

    # pobierz wartość parematru latitude i zapisz do zmiennej globalnej LAT, podanie większej ilości wartości przez
    #  użytkownika będzie ignorowane - zostanie pobrana tlyko pierwsza wartość
    # jeżeli został podany parametr -lat to przepisz wartość do zmiennej globalnej LAT, jak nie został podany, czyli
    #  domyślnie jest None to pomiń ten krok i pozostaw niezmienioną wartość LAT
#    if args.latitude is not None:
#        LAT = args.latitude[0]

# Jeżeli użytkownik nie podał argumentów, albo podał je błędnie to rozpocznij program od standardowego menu
#
# osobny 'if' zamiast komendy 'else' do poprzedniego 'if'a' z powodu, że gdy użytkownik źle przekaże argumenty to
#  pozostaje możliwość skorzystania ze standardowego menu (wcześniejszy blok kodu ustawi number_of_arguments = 0, co
#  oznacza, że coś poszło nie tak, ale użytkownik chce skorzystać z standardowego menu)
if number_of_arguments <= 1:

    # menu startowe
    print("""Weather to Excel
Tutaj możesz sprawdzić aktualną pogodę dla danego miejsca oraz aktualne zanieczysczenie powietrza, albo sprawdzić
prognozę pogody.
    
Co chcesz zrobić?
  1. Pokaz aktualne dane.
  2. Pokaż prognozę pogody.
  3. Ostatnio wyszukiwane.
  4. Zakończ działanie programu.
""")

    option = ""  # resetuję zmienną

    # wykonuj pętlę dopóki użytkownik nie poda prawidłowego numeru opcji
    while option != "1" and option != "2" and option != "3" and option != "4":
        # użytkownik pworwadza numer komendy - numer jest w postaci string, aby uniknąć błędów związanych z podaniem
        #  nieprawdiłowego znaku lub ciągu znaków
        option = input("Wprowadź numer opcji (1/2/3/4) i naciśnij ENTER: ")

        # sprawdź czy podana opcja jest poprawna, jeżeli nie to wyświetl komunikat o złym wyborze
        if option != "1" and option != "2" and option != "3" and option != "4":
            print("\nNie ma takiej opcji! Spróbuj jeszcze raz...\n")

    # dalej zbieram potrzebne informacje do wyświetlenia danych
    if option == "1":
        MODE = "current"  # tryb pokazywania aktualnych danych
        print("Aktualne dane\n")

        # funkcja pobiera zmienne globalne, użytkownik wprowadza miejsce, dla którego chce otrzymać informacje pogodowe
        #  i funkcja zwraca wskazane miejsce ponownie do zmiennych globalnych
        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

    elif option == "2":
        MODE = "forecast"  # tryb pokazywania prognozy pogody
        print("Prognoza pogody\n")

        CITY, LON, LAT = get_place_from_user(CITY, LON, LAT)

    elif option == "3":
        print("Ostatnio wyszukiwane\n")
        # TODO wykonać funkcję pobierania infromacji o ostatnim wyszukiwaniu

    elif option == "4":
        print("Zakończono działanie programu.")
        exit()

    else:
        print("Coś poszło nie tak przy wybieraniu opcji!")
        exit()  # kończy natychmiast program aby uniknąć potencjalnych błedów z powodu wybrania opcji, której nie ma

# kontrolny wydruk zmiennych podanych przez użytkownika
print("")
print("Kontrolny wydruk zmiennych")
print("CITY: ", CITY)
print("LON: ", LON)
print("LAT: ", LAT)
