#!/usr/bin/python

# Moduł zawierający funkcje wspomagające komunikację z użytkownikiem.
# Stworzona by utrzymacz czystość i przejrzystość w weather2excel.py


def check_GPS_value_from_user(data_from_user, MIN_expected_value, MAX_expected_value):
    # pobieram dane dla współrzędnej geograficznej, oczekuję liczby w zakresie od MIN_expected_value do
    #  MAX_expected_value (dla longitude 0-180, dla latitude 0-90)
    # funkcja zwraca w kolejności: type_is_correct, range_is_correct, value_GPS

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

        # TODO funkcja pobierająca współrzędne GPS wskazanej miejscowości i zwracająca je do longitude i latitude

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

        # koniec pobierania SZEROKOŚCI geograficznej

    # zwróć wartości zmiennych
    return city_name, longitude, latitude

# koniec funkcji get_place_from_user()
