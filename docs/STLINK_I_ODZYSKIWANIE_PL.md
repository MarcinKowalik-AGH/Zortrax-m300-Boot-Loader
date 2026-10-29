# ST-Link: v1.1 i awaryjne odtworzenie OEM

To droga serwisowa, nie rutynowy test działającej drukarki. Osobnego sprzętowego zapisu v1.1 przez SWD nie potwierdzono. Najpierw wykonaj [dwie zgodne kopie](KOPIA_ORYGINALU_PL.md) i sprawdź profil. Nie używaj cudzych danych.

## Pakiet STLINK

Zawiera 28672 B stage2 pod 0x08001000, 12288 B zasobów pod 0x0803A000, sparse HEX wyłącznie tych zakresów, RESTORE.BIN oraz lokalny generator. **Po masowym kasowaniu same te komponenty nie wystarczą**: brakuje prefixu OEM i danych egzemplarza. Nie wgrywaj surowo Update.bin, M300APP.M3B ani RESTORE.BIN.

## Własny obraz — bez połączenia z drukarką

Z rozpakowanego katalogu STLINK:

```sh
python3 prepare_stlink.py --backup "/wlasny/backup" --mode m300 --out "$HOME/Desktop/M300_PERSONAL_V11"
```

Powrót do OEM wymaga własnej kopii, która rzeczywiście zawiera oryginalny OEM:

```sh
python3 prepare_stlink.py --backup "/wlasny/backup_OEM" --mode oem --out "$HOME/Desktop/M300_PERSONAL_OEM"
```

Oczekiwane PASS_PERSONAL_IMAGE_OFFLINE. Powstaje nowy prywatny BIN 262144 B, HEX, manifest i sumy. Narzędzie nie otwiera portów ani nie zapisuje MCU; odmawia nadpisania katalogu i niezgodnej tożsamości. Zachowuje początek OEM oraz końcowe 8 KiB. To rekonstrukcja, nie dawny nienaruszony zrzut; licznik/ustawienia odpowiadają wybranej kopii.

## Połączenie i ochrona

Przy wyłączonym zasilaniu połącz zweryfikowane SWDIO, SWCLK, GND, referencję 3,3 V i NRST. TX/RX VCP nie zastępują SWD. Nie doprowadzaj 5 V ani nie zgaduj numeracji złącza z Inventure. CubeProgrammer: ST-LINK/SWD, Under reset, Hardware reset, początkowo 400 kHz. Under reset wymaga przewodu NRST. Sprawdź napięcie, ID oraz opcje; błąd połączenia nie uzasadnia kasowania.

**Wyłączenie aktywnego RDP STM32F1 masowo kasuje główną Flash, BOOT i NVM/factory.** Read Unprotect jest dozwolone dopiero jako świadome odzyskiwanie z gotowego pełnego osobistego obrazu, nie metoda backupu. Surowe A5 oznacza brak ochrony, 00 ochronę aktywną; nie stosuj AA z F2/Inventure. Gdy RDP już wyłączone, nie ponawiaj odblokowania.

Po przeładowaniu opcji połącz się ponownie i porównaj UID/SIZE z własną kopią. Nie programuj UID, SIZE ani SYSROM. Nie wgrywaj surowego OPTIONS.bin jako obrazu Flash. Sprawdź pozostałe opcje względem zapisanego stanu. Podczas zapisu i readback pozostaw RDP nieaktywne.

## Programowanie

Wybierz wygenerowany pełny PERSONAL BIN: adres **0x08000000**, długość **0x40000**. Verify włączone, automatyczne Run wyłączone, Skip erase wyłączone. Nie przerywaj zapisu. Po weryfikacji, z zatrzymanym MCU, odczytaj cały zakres do READBACK.bin i porównaj cmp oraz SHA-256 z osobistym obrazem. Wymagane są identyczne bajty.

Dopiero potem zakończ debug, wyłącz zasilanie, odłącz programator i uruchom bez karty aktualizacyjnej. Sprawdź menu, hardware, własny serial i licznik przed drukiem/grzaniem. Procedura nie naprawia uszkodzeń elektroniki i nie zapewnia odzyskania po każdej awarii.

Źródła: [ST PM0075](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf), [CubeProgrammer CLI](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_Command_Lines.html).
