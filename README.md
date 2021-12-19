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
    - [ ] Opisno vprašanje ne preverja pravilnosti (ali sploh rabimo glede na to da je opisno vprašanje lahko oblike *Opiši dogodek z lastnimi besedami*)
    - [ ] Točkovanje
    - [x] Ko izpolnjuješ vprašanja na kvizu mora avtomatsko na naslednje vprašanje
    - [ ] Dobimo ime mesta po imenu v leafletu



Po prototipu
- [ ] Logično redirectanje
- [ ] Številčenje vprašanj v kvizu (želimo po vrsti)
- [ ] Brisanje in urejanje že obstoječih kvizov oz. vprašanj
- [ ] Uporabniki in piškotki?
- [ ] Login System (učenci ne smejo imeti dostopa do urejanja vprašanj --- učenec mora imet opcijo da naredi kviz in ga potem tudi ureja (ureja lahko samo ta kviz ki ga je on kreiral)
- [ ] Bootstrap  
- [ ] Styling
