# weather2excel [![Build Status](https://travis-ci.org/gdaPythonProjects/weather2excel.svg?branch=master)](https://travis-ci.org/gdaPythonProjects/weather2excel)
W celu wykorzystnia aplikacji należy zarejestorwać się w co najmniej jednym z 8 serwisów:
<table>
 <tr>
  <td><a href='https://www.apixu.com' target='_blank'><img src='logo/apixu.png'></a></td>
  <td><a href='https://darksky.net' target='_blank'><img src='logo/darksky.png'></a></td>
  <td><a href='https://www.weatherbit.io' target='_blank'><img src='logo/weatherbit.png'></a></td>
  <td><a href='https://openweathermap.org' target='_blank'><img src='logo/openweathermap.png'></a></td>
 </tr>
 <tr>
  <td><a href='http://aqicn.org' target='_blank'><img src='logo/waqi.jpeg'></a></td>
  <td><a href='https://www.climacell.co' target='_blank'><img src='logo/climacell.png'></a></td>
  <td><a href='https://airly.eu' target='_blank'><img src='logo/airly.jpg'></a></td>
  <td><a href='https://www.airvisual.com' target='_blank'><img src='logo/airvisual.png'></a></td>
 </tr>
 </table>
 1. https://www.apixu.com <br>
 2. https://darksky.net <br>
 3. https://www.weatherbit.io <br>
 4. https://openweathermap.org <br>
 5. http://aqicn.org <br>
 6. https://www.climacell.co <br>
 7. https://airly.eu <br>
 8. https://www.airvisual.com<br>
<br>
Klucz/token do korzystania z danego API powinien zostać dopisany w odpowiednim pliku w /config/API_keys/.<br>
Prognozy i bieżące wyniki będą podawane w czasie UTC. Aby uzyskać je w czasie lokalnym dla wyszukiwanych miejsc, należy skonfigurować co najmniej jednen z serwisów: APIXU, DarkSky.
<br>Tabela przedstawiająca ogólne możliwe do wykorzystania funkcjonalności Weather API<br>
<img src='logo/tabela_api.png'>

<br><br>
Geokodowanie odbywa się za pomocą:<br>
<a href='https://www.openstreetmap.org' target='_blank'><img src='logo/OpenStreetMap_logo.jpg' width='126' height='90'></a>
<br>

# Zależności:
    pip3 install unit-converter
    pip3 install --upgrade jsonpath-ng
    pip3 install requests
    pip3 install python-dateutil

# Uruchomienie
    python3 weather2excel.py

Wyjaśnienie symboli w wynikach:\
<span> <b>*</b>  API nie oferuje danych</span>\
<span> <b>#</b>  dane chwilowo niedostępne</span>\
<span> <b>_</b>  problem z konwersją danych</span>\
<span> <b><</b>  wartość poniżej dopuszczalnego przedziału</span>\
<span> <b>></b>  wartość powyżej dopuszczalnego przedziału</span>
