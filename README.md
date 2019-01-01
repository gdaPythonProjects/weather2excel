# weather2excel
W celu wykorzystnia aplikacji należy zarejestorwać się w co najmniej jednym z serwisów:
 1) https://www.apixu.com
 2) https://darksky.net
 3) https://www.weatherbit.io
 4) https://openweathermap.org
 5) http://aqicn.org

Klucz/token do korzystania z danego API powinien zostać zapisany w odpowiednim pliku w /config/API_keys/.

#Zależności:
pip3 install unit-converter
pip3 install --upgrade jsonpath-ng

#Uruchomienie
python3 weather2excel.py

Wyjaśnienie symboli w wynikach:
* API nie oferuje danych
# dane chwilowo niedostępne
- problem z konwersją danych

