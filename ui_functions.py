#!/usr/bin/python

# Moduł zawierający funkcje wspomagające komunikację z użytkownikiem.
# Stworzona by utrzymacz czystość i przejrzystość w weather2excel.py


# Zwróć szerokość i długość geograficzną podanego miasta
# funkcja zwraca w kolejności: LON, LAT
def get_coords_by_city_name(CITY, COUNTRY):
    import geocoder

    # wybór w menu miast
    choice = 0

    geocoder = geocoder.geocoder()

    # zwróć ilość miast o takiej samej nazwie
    num_results = geocoder.getQueryResults(CITY, COUNTRY)

    # jeżeli jest ich więcej niż 1 to daj użytkownikowi wybór, dla któ©ego miasta chce uzyskać dane
    if num_results >= 1:

        geocoder.listResults()

        # powtarzaj póki użytkownik nie poda prawidłowego numeru miasta
        while not isinstance(choice, int) or choice < 0 or choice > num_results - 1:
            option = input("Wybierz numer z właściwym miejscem i naciśnij ENTER: ")
            try:
                choice = int(option) - 1
            except:
                print("Nie wprowadzono prawidłowej wartości z przedziału <1;" + num_results + ">")

    # jeżeli zwrócono ilość miast 0 lub liczbę ujemną (oznacza błąd)
    elif num_results < 1:
        print("Nie udało się wyznaczyć współrzednych dla podanej frazy wyszukiwania.")
        print("Proszę spróbować wyszukiwania dla innej frazy lub za pomocą współrzednych geograficznych.")
        quit()

    # pobierz koordynaty dla wybranego miasta
    coord = geocoder.getCoordindates(choice)

    # jeżeli zwrócono False to znaczy, że wystąpił jakiś błąd
    if coord is False:
        print("Nie udało się uzyskać współrzędnych wybranej miejscowości.")
        print("Proszę spróbować wyszukiwania dla innej frazy lub za pomocą współrzednych geograficznych.")
        quit()

    # zwróć koordynaty jeżeli wszsytko poszło dobrze
    return coord["lon"], coord["lat"]


# pobieram dane dla współrzędnej geograficznej, oczekuję liczby w zakresie od MIN_expected_value do
#  MAX_expected_value (dla longitude 0-180, dla latitude 0-90)
# funkcja zwraca w kolejności: type_is_correct, range_is_correct, value_GPS
def check_GPS_value_from_user(data_from_user, MIN_expected_value, MAX_expected_value):
    range_is_correct = 0
    value_GPS = None

    try:
        # jeżeli użytkownik użył przecinka do oddzielenia części całości od ułamkowej to zamień go na kropkę
        if "," in data_from_user:
            data_from_user = data_from_user.replace(",", ".")

        # konwertuj do typu float i zobacz czy wyskoczy błąd
        value_GPS = float(data_from_user)

    except ValueError:
        # jeżeli nie da się konwertować do float to ustaw flagę type_is_correct na 0
        type_is_correct = 0

    else:  # jeżeli pójdzie dobrze oznacz type_is_correct na 1 jako prawidłowy
        type_is_correct = 1

    # jeżeli typ jest poprawny (float) to sprawdź, czy jest w prawidłowym zakresie
    if type_is_correct == 1:

        if MIN_expected_value < value_GPS < MAX_expected_value:
            # jezeli wartość jest w prawidłowym zakresie to ustaw range_is_correct na 1
            range_is_correct = 1

        else:
            # jeżeli jest poza zakresem to ustaw range_is_correct na 0 oraz wyczyść wartość value_GPS
            range_is_correct = 0
            value_GPS = None

    # zwróć informację czy typ oraz zakres jest prawidłowy oraz przetworzoną wartość współrzędnej GPS
    #  (tylko jak jest poprawna, w innym wypadku zwróć None
    return type_is_correct, range_is_correct, value_GPS

# koniec check_GPS_value_from_user()


# funkcja pobierająca dane o miejscu od użytkownika i zmieniająca odpowiednie zmienne dla API pogodowych
def get_place_from_user(city_name, longitude, latitude):
    import geocoder

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
        city_name = input("\nPodaj miasto: ").lower()  # małe litery dla ułatwienia komunikacji z API

        longitude, latitude = get_coords_by_city_name(city_name, "")

    elif option == "2":

        # pobieram dane dla DŁUGOŚCI geograficznej (longitude), oczekuję liczby w zakresie od 0 do 180

        isCorrectValue = 0  # flaga informująca, czy użytkownik prawidłowo wprowadził dane
        isCorrectRange = 0  # flaga określająca, czy podana przez użytkownika wartość mieści się w zakresie

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowo współrzędnej długości geograficznej
        while isCorrectRange != 1 or isCorrectValue != 1:

            tmp_longitude = input("Podaj długość geograficzną (w formie ułamka dziesiętnego od 0 do 180): ")
            isCorrectValue, isCorrectRange, longitude = check_GPS_value_from_user(tmp_longitude, 0, 180)

            if isCorrectValue == 0:
                print("Nieprawidłowy format współrzędnej! Pamiętaj, że ma być liczbą dziesiętną!\n")

            elif isCorrectValue == 1 and isCorrectRange == 0:
                print("Wartość poza zakresem! Spróbuj jeszcze raz!")

        # jeżeli użytkownik podał równe 180 stopni zamieniam je na 0, aby poprawnie wprowadzić współrzędne do API
        #  nie każde API może prawidłowo przyjąć wartość 180 i większą
        if longitude == 180:
            longitude = 0

        # koniec pobierania DŁUGOŚCI geograficznej

        # pobieram dane dla SZEROKOŚCI geograficznej (longitude), oczekuję liczby w zakresie od 0 do 180

        isCorrectValue = 0  # reset flagi
        isCorrectRange = 0  # reset flagi

        # wykonuj pętlę dopóki użytkownik nie poda prawidłowo współrzędnej szerokości geograficznej
        while isCorrectRange != 1 or isCorrectValue != 1:

            tmp_latitude = input("Podaj szerokość geograficzną (w formie ułamka dziesiętnego od 0 do 90): ")
            isCorrectValue, isCorrectRange, latitude = check_GPS_value_from_user(tmp_latitude, 0, 90)

            if isCorrectValue == 0:
                print("Nieprawidłowy format współrzędnej! Pamiętaj, że ma być liczbą dziesiętną!\n")

            elif isCorrectValue == 1 and isCorrectRange == 0:
                print("Wartość poza zakresem! Spróbuj jeszcze raz!\n")

        # jeżeli użytkownik podał równe 90 stopni zamieniam je na 0, aby poprawnie wprowadzić współrzędne do API
        #  nie każde API może prawidłowo przyjąć wartość 180 i większą
        if latitude == 90:
            latitude = 0

        g = geocoder.geocoder()
        place = g.getQueryReverseResults(latitude, longitude)

        city_name = place['city']
        # koniec pobierania SZEROKOŚCI geograficznej

    # zwróć wartości zmiennych
    return city_name, longitude, latitude

# koniec funkcji get_place_from_user()


# wyświetl wiadomość powitalną
def welcome_message():
    print("""
Weather to Excel
Tutaj możesz sprawdzić aktualną pogodę dla danego miejsca oraz aktualne zanieczysczenie powietrza, albo sprawdzić
prognozę pogody.""")

# koniec funkcji welcome_message()


# sprawdź czy Użytkownik podał wartość, która jest na liście
# zwróć None jeżeli nie ma takiej wartości, zwróć tą wartość jeżeli występuje
def check_user_choice_is_correct(data_from_user, choices):

    # flaga określająca, czy wartość występuje na liście, założenie początkowe, że nie (dlatego 0)
    correct_choice = 0

    # sprawdź czy wartośc występuje na liście, jeżeli tak to przerwij pętlę
    for option in choices:
        if option == data_from_user:
            correct_choice = 1
            break

    if correct_choice == 0:
        return None
    else:
        return data_from_user
