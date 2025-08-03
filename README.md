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

- Etusivulla löytyy linkit käyttäjätunnuksen luontiin, kirjautumiseen sekä kasvien etsimisiseen.

  ![etusivu](//kasvisto/static/images/kasvisto-index.jpg)

- Kirjautumisen jälkeen käyttäjä voi lisätä, muokata ja poistaa kasveja sekä lisätä hoitotietoja.
- Käyttäjä voi hakea lisättyjä kasveja ja niiden hoitotietoja myös kirjautuneena.

  ![kirjautunut](//kasvisto/static/images/kasvisto-kirjautunut.jpg)

- Käyttäjä sivulla näkyvät lisätyt käyttäjän lisäämät kasvit

  ![kasvit](//kasvisto/static/images/kasvisto-kayttaja.jpg)

## Sovelluksen toiminnot

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy lisämään, muokkaamaan ja poistamaan kasveja sovelluksessa.
- [x] Käyttäjä pystyy lisäämään kasveille hoitotietoja esim. kastelut.
- [ ] Käyttäjä pysyy lisäämään kuvia kasveihin.
- [x] Käyttäjä näkee sovellukseen lisätyt kasvit sekä niiden hoitotiedot.
- [x] Käyttäjä pystyy hakemaan lisäämiään kasveja sekä niiden hoitotietoja.
