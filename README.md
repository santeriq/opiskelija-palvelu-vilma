Yritin saada tämän toimimaan fly.io mutta en saanut

website -> __init__.py
- "SECRET_KEY" tarvisee arvon, jätin .env tiedoston pois jossa se sijaitsee
- "DATABASE_URL" tarvisee arvon, jätin .env tiedoston pois jossa se sijaitsee

schema.sql
- valmiit komennot joilla luot taulukot ja lisäät niihin testitapauksia


Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ venv/Scripts/activate  (windows, ainakin minulla))
$ pip install -r requirements.txt (päivitetty 27.3.2023)
Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run

--------------------

Valmiit testikäyttäjät:
- admin1 (admin)
- teacher1 (teacher) (not ready)
- student1 (student) (not ready)
- user1 (guest)

Salasana: 
- password1


Admin:
- pystyy luomaan kursseja (valmis)
- pystyy muokkaamaan kurrseja (valmis)
- pystyy näkemään olemassa olevat kurssit (valmis)
- pystyy hyväksymään/hylkäämään opiskelijapyynnön (ei vielä toimiva)
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
