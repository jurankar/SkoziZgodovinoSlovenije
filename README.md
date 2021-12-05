# Skozi zgodovino Slovenije

Spletna aplikacija za interaktivne kvize in učenje zgodovine Slovenije na zabaven način.

## Tabele:
- `dbQuiz`: podatki o kvizu
- `dbQuestion`: celotna vsebina vprašalne strani
- `dbAnswers`: odgovori na vprašanja

## Url:
- `/`: začasna stran za povezave na druge
- `/test_map`: začasna stran za Leaflet (tu začnemo s kvizi)
- `/quiz_manager`: ogled, urejanje, brisanje kvizov
- `/add_quiz`: ustvari nov kviz
- `/add_question`: izberemo ime in tip novega vprašanja
- `/add_question_type`: forms, glede na prej izbran tip

## Kaj je še treba implementirati / popraviti
- [x] Models
- [x] Forms
- [x] Dodajanje kvizov in vprašanj (osnovno)
- [ ] Foreign key ne deluje v formsih (zaenkrat samo Char) ->  Maj
- [ ] Povezava kviz <-> vprašanje: torej, po kliku na kviz dodamo vprašanje tistemu kvizu + ko ustvarimo kviz nas preusmeri direkt na dodajanje novega vprašanja ->  Maj
- [ ] Upload slik (rešitev) + implementacija v forme -> Maj če se mu da
- [ ] Podajanje parametra med viewsi (preko templateov) -> Maj
- [ ] Leaflet na urejanje, dodajanje in brisanje -> Jan
- [ ] Združevanje `add_question` in `add_question_type`: reactive glede na to, katero vrsto vprašanja izberemo -> Jan
- [ ] Kviz 



Po prototipu
- [ ] Logično redirectanje
- [ ] Številčenje vprašanj v kvizu (želimo po vrsti)
- [ ] Brisanje in urejanje že obstoječih kvizov oz. vprašanj
- [ ] Uporabniki in piškotki?
- [ ] Bootstrap  
- [ ] Login System (učenci ne smejo imeti dostopa do urejanja vprašanj)
- [ ] Styling
