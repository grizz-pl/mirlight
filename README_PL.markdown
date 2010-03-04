Mirlight by Witold Firlej
=========================

## Ręcznej roboty ;) ambilight 
### strona domowa programu [PL] <http://grizz.pl/mirlight>
### github [EN / PL] <http://github.com/grizz-pl/mirlight/>
### strona dt. sprzętu [PL] <http://mirley.firlej.org/mirlight>

Uwaga
-----

### PL
Mirlight występuje w dwóch wersjach sprzetu. Oprogramowanie uzywające starej wersji umieszczone jest w gałęzi **old_hardware_version** i nie jest juz rozwijane.  
Nowa wersja (>= 0.5) jest umieszczona w gałezi **master**.

Wymagania
---------

*  python 2.6
*  Qt 4.5
*  pyQt
*  pyserial <http://pyserial.wiki.sourceforge.net/pySerial>

Więcej informacji
-----------------

Informacje na temat projektu będą zapewne pojawiać się na <http://grizz.pl/> - ten program i <http://mirley.firlej.org> - część sprzętowa.

### Szybki start dla użytkowników Linuksa

1. Zainstaluj wymagane pakiety
2. Uruchom `./mirlight`

### Szybki start dla użytkowników Windows®

#### binarka

1. Pobierz plik .zip ze strony <http://github.com/grizz-pl/mirlight/downloads>
2. Rozpakuj
3. Uruchom mirlight_gui.exe

#### wersja ze źródeł

1. Ściągnij i zainstaluj [ActivePython](http://www.activestate.com/store/download.aspx?prdGUID=b08b04e0-6872-4d9d-a722-7a0c2dea2758)
2. Ściągnij i zainstaluj [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download) Pobieramy oczywiście *Windows Installer*
3. Ściągnij i zainstaluj [Pyserial](http://sourceforge.net/projects/pyserial/files/)
4. Pobierz **mirlight** używając `git clone git://github.com/grizz-pl/mirlight.git` [HowTo](http://github.com/guides/using-git-and-github-for-the-windows-for-newbies) albo pobierz archiwum używając linków z zakładek u góry strony.
5. Wejdź w katalog **mirlight** i uruchom `mirlight.bat` albo `mirlight_verbose.bat` (druga opcja wyświetla kilka przydatnych informacji w okienku cmd)
