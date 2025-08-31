# KASVISTO 🪴

_HY Tietokannat ja web-ohjelmointi-kurssin projektityö: Kasvien hoitopäiväkirja_

## Sovelluksen asennus

- Projektin kloonaus omalle koneelle:

```
$ git clone https://github.com/mkekola/kasvisto.git
```

- Siirry projektin hakemistoon:

```
$ cd kasvisto
```

- Luo projektille Python-virtuaaliympäristö:

```
$ python -m venv venv
```

- Aktivoi virtuaaliympäristö:

```
$ source venv/bin/activate
```

- Asenna flask-kirjasto:

```
$ pip install flask
```

- Luo tietokanta _database.db_:

```
$ sqlite3 database.db < schema.sql
```

- Käynnistä sovellus:

```
$ flask run
```

## Sovelluksen käyttäminen

- Etusivulla löytyy linkit käyttäjätunnuksen luontiin, kirjautumiseen sekä kasvien etsimisiseen ja listaus lisätyistä kasveista.
- Kirjautumisen jälkeen käyttäjä voi lisätä, muokata ja poistaa kasveja sekä lisätä hoitotietoja.
- Käyttäjä voi hakea lisättyjä kasveja myös kirjautuneena.
- Käyttäjä sivulla näkyvät lisätyt käyttäjän lisäämät kasvit ja lukumäärä.
- Kasvin sivulla näkyvät kasvin tiedot, hoitotiedot ja kuvat.
- Kommentit näkyvät kasvin sivulla, jossa käyttäjä voi lisätä omia kommenttejaan.


## Sovelluksen toiminnot

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisämään, muokkaamaan ja poistamaan kasveja sovelluksessa.
- [x] Käyttäjä pystyy lisäämään kasveille hoitotietoja esim. kastelut.
- [x] Käyttäjä pystyy lisäämään kuvia kasveihin.
- [x] Käyttäjä näkee sovellukseen lisätyt kasvit sekä niiden hoitotiedot.
- [x] Käyttäjä pystyy hakemaan lisäämiään kasveja sekä niiden hoitotietoja.
- [x] Käyttäjä pystyy lisäämään kommentteja omiin ja muiden lisäämiin kasveihin.
