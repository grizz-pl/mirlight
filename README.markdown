Mirlight by Witold Firlej
=========================

## Homemade ambilight not only for films
### homepage  [PL only] <http://grizz.pl/mirlight>
### page on github [EN / PL] <http://github.com/grizz-pl/mirlight/>
### hardware homepage [PL only] <http://mirley.firlej.org/mirlight>

Pay attention
-------------

### EN
Mirlight has two hardware versions. Software useing an old one is placed in branch **old_hardware_version** and it isn't developed anymore.  
A new version (>= 0.5) is placed in branch **master**.

### PL
Mirlight występuje w dwóch wersjach sprzetu. Oprogramowanie uzywające starej wersji umieszczone jest w gałęzi **old_hardware_version** i nie jest juz rozwijane.  
Nowa wersja (>= 0.5) jest umieszczona w gałezi **master**.

Requirements
------------

*  python 2.6
*  Qt 4.5
*  pyQt
*  pyserial <http://pyserial.wiki.sourceforge.net/pySerial>

More info
---------

blah ;)

### EN

#### Quickstart for Linux users

1. Install required packages
2. Run `./mirlight`

#### Quickstart for Windows® users

1. Download and install [ActivePython](http://www.activestate.com/store/download.aspx?prdGUID=b08b04e0-6872-4d9d-a722-7a0c2dea2758)
2. Download and install [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download) Downloading  *Windows Installer*
3. Download and install [Pyserial](http://sourceforge.net/projects/pyserial/files/)
4. Get **mirlight** using `git clone git://github.com/grizz-pl/mirlight.git` [HowTo](http://github.com/guides/using-git-and-github-for-the-windows-for-newbies) or download an archive usings links above.
5. Go to mirlight directory and run `mirlight.bat` or `mirlight_verbose.bat` (second one display some useful informations in cmd window)

### PL
Informacje na temat projektu będą zapewne pojawiać się na <http://grizz.pl/> - ten program i <http://mirley.firlej.org> - część sprzętowa.
#### Szybki start dla użytkowników Linuksa

1. Zainstaluj wymagane pakiety
2. Uruchom `./mirlight`

#### Szybki start dla użytkowników Windows®

1. Ściągnij i zainstaluj [ActivePython](http://www.activestate.com/store/download.aspx?prdGUID=b08b04e0-6872-4d9d-a722-7a0c2dea2758)
2. Ściągnij i zainstaluj [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download) Pobieramy oczywiście *Windows Installer*
3. Ściągnij i zainstaluj [Pyserial](http://sourceforge.net/projects/pyserial/files/)
4. Pobierz **mirlight** używając `git clone git://github.com/grizz-pl/mirlight.git` [HowTo](http://github.com/guides/using-git-and-github-for-the-windows-for-newbies) albo pobierz archiwum używając linków z zakładek u góry strony.
5. Wejdź w katalog **mirlight** i uruchom `mirlight.bat` albo `mirlight_verbose.bat` (druga opcja wyświetla kilka przydatnych informacji w okienku cmd)

Changelog
---------
### ver.0.5beta 2010/01/25
(based on  var. d.2010.01.25.1)

*  GUI changes
*  New color algorithm
*  Showing and set fields
*  Verbose mode


### ver.0.5alfa 2009/11/15

*  Switch to a new hardware.

### ver.0.25 2009/03/29

*  Making average color for each screen region is much better.

### ver.0.2 2009/03/29

*  All basic functions work.
