# weather2excel
W celu wykorzystnia aplikacji należy zarejestorwać się w co najmniej jednym z serwisów:
 1) https://www.apixu.com ![Logo](icons/apixu.png)
 2) https://darksky.net
 3) https://www.weatherbit.io
 4) https://openweathermap.org
 5) http://aqicn.org
 6) https://www.climacell.co/

Klucz/token do korzystania z danego API powinien zostać zapisany w odpowiednim pliku w /config/API_keys/.

# Zależności:
> pip3 install unit-converter\
> pip3 install --upgrade jsonpath-ng\
> pip3 install requests

# Uruchomienie
> python3 weather2excel.py

Wyjaśnienie symboli w wynikach:\
<span> <b>*</b>  API nie oferuje danych</span>\
<span> <b>#</b>  dane chwilowo niedostępne</span>\
<span> <b>_</b>  problem z konwersją danych</span>\
<span> <b><</b>  wartość poniżej dopuszczalnego przedziału</span>\
<span> <b>></b>  wartość powyżej dopuszczalnego przedziału</span>
