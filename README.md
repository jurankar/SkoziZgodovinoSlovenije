# Skozi zgodovino Slovenije

Spletna aplikacija za interaktivne kvize in učenje zgodovine Slovenije na zabaven način.

## Tabele:
- `dbQuiz`: podatki o kvizu
- `OpisnoModel`: vprašanja "opisnega" tipa
- `PravilnoNepravilnoModel`: vprašanja tipa "P/N"
- `IzberiOdgovorModel`: vprašanja tipa "izberi pravilno možnost"
- `dbAnswers`: odgovori na vprašanja

## Url:
- `/`: začasna stran za povezave na druge
- `/test_map`: začasna stran za Leaflet (tu začnemo s kvizi)
- `/quiz_manager`: ogled, brisanje vseh kvizov na splošno
- `/add_quiz`: ustvari nov kviz
- `/add_question`: izberemo ime in tip novega vprašanja glede na kviz
- `/delete_question`: izbriše vprašanje
- `/delete_quiz`: izbriše kviz

## Kaj je še treba implementirati / popraviti
- [x] Models
- [x] Forms
- [x] Dodajanje kvizov in vprašanj (osnovno)
- [x] Foreign key ne deluje v formsih (zaenkrat samo Char) ->  Maj
- [x] Povezava kviz <-> vprašanje: torej, po kliku na kviz dodamo vprašanje tistemu kvizu + ko ustvarimo kviz nas preusmeri direkt na dodajanje novega vprašanja ->  Maj
- [x] Upload slik (rešitev) + implementacija v forme -> Maj
- [x] Podajanje parametra med viewsi (preko templateov) -> Maj
- [x] Leaflet na urejanje, dodajanje in brisanje -> Jan
- [x] Združevanje `add_question` in `add_question_type`: reactive glede na to, katero vrsto vprašanja izberemo -> Jan
- [x] Kviz
    - [x] Opisno vprašanje ne preverja pravilnosti (ali sploh rabimo glede na to da je opisno vprašanje lahko oblike *Opiši dogodek z lastnimi besedami*)
    - [x] Točkovanje
    - [x] Ko izpolnjuješ vprašanja na kvizu mora avtomatsko na naslednje vprašanje
    - [x] Dobimo ime mesta po imenu v leafletu --> Jan
    - [x] Vprašanja se soltirajo po času --> Maj
    - [x] Letnice na časovni trak --> Jan
    - [x] Na točkovanje vsa vprašanja, ne samo tistih, ki jih je uporabnik rešil --> Maj

Po prototipu
- [x] Logično redirectanje
- [x] Brisanje in urejanje že obstoječih kvizov oz. vprašanj --> Maj
- [x] Login System (učenci ne smejo imeti dostopa do urejanja vprašanj --- učenec mora imet opcijo da naredi kviz in ga potem tudi ureja (ureja lahko samo ta kviz ki ga je on kreiral) --> Maj
- [x] Styling  --> Jan
- [x] Vprašanja z izberi odgovoro morjo met poljubno število možnosti (preveč dodatnega dela)
- [x] Ne gre izbrisati slike iz vprašanja -> Maj
- [x] Večji text fieldi za opise -> Maj
- [x] Uporabniki si ne smejo izbrati istega nadimka kot že nekdo prej na istem kvizu

Styling:
- [x] pri obrazcih za vprašanja je treba skriti polji `longitude` in `latitude`, saj se samodejno izpoljenjo s pomočjo zemljevida
- [x] mapa in search bar na sredino pri obrazcih za dodajanje vprašanj
- [x] več prostora med labeli in formsi (skoraj povsod)
- [x] letnice vprašanj na vrh zaznamkov na časovnem traku (! POMEMBNO, je rekel Batagelj da je treba)
- [x] `Končaj poskus` gumb padding levo
- [x] poravnava krogcev in odgovorov pri izbirnih vprašanjih (! POMEMBNO)
- [x] poravnava formsov ob prijavi ali registraciji
- [x] velikost slik v vprašanjih naj bo fiksna (da prevelike slike ne zasedejo celega okna)


TODO:
- [x] opisni odgovor: daljše okence
- [x] izbirni odgovor: poravnane pike z odgovori
- [x] `Get in touch` gumb remove
- [x] labeli na prijavi (`Password` -> `Geslo`)
- [x] pravilno-nepravilno: ko generiramo vprašanje manjše razmike med P in N
- [x] gumbi `Shrani` padding na dnu
- [x] stran `Navodila`
- [x] večja okenca za vprašanja
- [x] presledki pri odgovorih, izbirno vprašanje in p/n vprašanje
- [x] navodila za inštalacijo 


## Navodila za namestitev
1. Zaženit ukaz 'pip install -r requirements.txt'
2. Zaženite ukaz 'python .\manage.py runserver'
