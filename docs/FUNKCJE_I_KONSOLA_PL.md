# M300 boot v1.1 — funkcje i Hardware

Nagłówek: **M300 boot v1.1 © Marcin Kowalik**. © jest znakiem bitmapowym. Menu nie zawija się na końcach; Back jest przypięty w podmenu, lista przesuwa się o jeden wiersz, a enkoder i częściowe odświeżanie OLED zachowują płynność rc3.

Diagnostics → Hardware pokazuje po angielsku Model, Hardware version, Serial number oraz Total operating time. Hardware/serial/czas są odczytywane z rekordów drukarki przy każdym wejściu; model jest nazwą obsługiwanego profilu. Błędne rekordy pokazują Unavailable. Ekran czeka na następny klik i nie zapisuje NVM. Pośrednik i4 ma odpowiednik tego widoku.

Pierścień oblicza procent aktualnej fazy z bajtów, stron lub czasu przytrzymania. Osobna weryfikacja może ponownie zacząć się od 0%. Nieznany zakres ma --; błąd nie udaje 100%.

Zachowane: ręczny start, pięciosekundowy autostart przerywany wejściem, aktualizacje aplikacji SD/UART z weryfikacją, pomijanie identycznego obrazu, wybór pliku, kopie Flash/tożsamości, diagnostyka i historia 24 zdarzeń. To jeden wymienny slot aplikacji, nie gotowy port Klippera ani równoczesny dual-boot.

UART: 19200/57600/115200/250000/500000, 8N1 bez flow control. Ustawienie jest zapisane poza fabrycznym NVM. Przytrzymanie enkodera podczas startu daje awaryjny serwis 250000. Pośrednik ma tymczasowe 250000 i zachowuje dziennik boota. Fizyczne połączenie USART1: PA9/TX → RX adaptera, PA10/RX ← TX, GND, logika 3,3 V. Bez aktywnego SWD i 5 V. Nie utożsamiaj złącza z Inventure P4.

Publiczna konsola KONSOLA_M300_v1.1.command wymaga Python/pyserial i zapisuje prywatny log. --dump-all pobiera dwie kopie obsługiwanych zakresów. m300_service.py służy do odczytów i sprawdzania kopii/historii; ibtool.py do pakowania surowych aplikacji pod 0x08008000 i obsługi M3B, bez kluczy odszyfrowania OEM. Nie pakuj stage2 jako aplikacji i nie używaj starych skryptów rc3 --install do i4/v1.1.
