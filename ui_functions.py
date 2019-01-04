#!/usr/bin/python

# Moduł zawierający funkcje wspomagające komunikację z użytkownikiem.
# Stworzona by utrzymacz czystość i przejrzystość w weather2excel.py


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