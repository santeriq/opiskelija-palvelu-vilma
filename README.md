Yritin saada tämän toimimaan fly.io mutta en saanut

website -> __init__.py
- "SECRET_KEY" tarvitsee arvon, jätin .env tiedoston pois jossa se sijaitsee
- "DATABASE_URL" tarvisee arvon, jätin .env tiedoston pois jossa se sijaitsee

schema.sql
- valmiit komennot joilla luot taulukot ja lisäät niihin testitapauksia



!! HUOMIOITAVAA !!

Sovelluksessa on CSRF-haavoittuvuus (en kerennyt korjaamaan tätä, mahdollisesti myöhemmin)


Databasesta:

Sain palautetta:

"Sain useita virheitä yrittäessäni kirjautua tai luoda kursseja, ja jouduin antamaan postgres käyttäjälle oikeudet komennolla "GRANT (komentoja) ON (kohdetaulukko tai arvo) TO (käyttäjä)". Saattaa olla tarkoituksellista, mutta suosittelen kirjoittamaan ohjeet README:en jos sovellus ei mene fly.ioon."

Voi siis mahdollisesti olla ongelmia databasen kanssa, en tiedä mistä tämä johtuu.

Jouduin myös poistamaan REFERENCES yrittäessä siirtää sovellusta fly.io, tämän vuoksi schema.sql ei ole niitä

----------------------------
**Ohjeet**

1. Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon

2. Luo kansioon .env-tiedosto ja määritä sen sisältöön

DATABASE_URL=

SECRET_KEY=

3. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv

$ source venv/bin/activate TAI $ venv/Scripts/activate  (windows, ainakin minulla)

$ pip install -r requirements.txt

4. Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run

--------------------

Valmiit testikäyttäjät:
- admin1 (admin)
- teacher1 (teacher)
- student1 (student)
- user1 (guest)
- uesr2 (guest)

Salasana: 
- password1


Admin:
- pystyy luomaan kursseja
- pystyy muokkaamaan kurrseja
- pystyy näkemään olemassa olevat kurssit
- pystyy hyväksymään/hylkäämään opiskelijapyynnön
- pystyy lisäämään käyttäjille rooleja
- pystyy poistamaan palvelun käyttäjiä
- pystyy näkemään kaikki palvelun käyttäjät

Teacher:
- pystyy selaamaan kursseja
- pystyy liittymään/poistumaan kursseilta
- pystyy lisäämään suoritusmerkinnän ja arvosanan kurssista opiskelijalle

Student:
- pystyy selaamaan kursseja
- pystyy liittymään/poistumaan kursseilta
- pystyy näkemään omat opintosuorituksensa

Guest:
- pystyy luoda käyttäjän ja pyytää opiskelijaroolia
