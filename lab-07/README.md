# Lab 07 - Web Security


```js
sql = "SELECT * FROM table WHERE item = '" + user_input_variable + "' <other expressions>";
database.query(sql);
```

```js
user_input_variable = "' OR 1=1 -- "; // example input given by the user
sql = "SELECT * FROM table WHERE item = '' OR 1=1 -- ' <other expressions>";
```


## Task 1 | SQL Injection


Setup, pe **local**, nu pe VM :)
```sh
# First, start the MariaDB instance in background
$ docker run -d --rm --name database ghcr.io/cs-pub-ro/isc-lab-web-db
# Wait until the DB server fully starts:
$ docker logs database -f 
# Ctrl+C and continue when it says: 'mariadbd: ready for connections.'
 
# Finally, start the lab's web server
$ docker run -it --link database:database -p 8080:8080 ghcr.io/cs-pub-ro/isc-lab-web-app
```


> Reminder: querry language-ul folosit este `MariaDB`.

Pentru a ma loga la user-ul **admin**, am facut urmatorul **SQL injection**:
(dupa comentariu `--`, obligatoriu se pune spatiu !)

```sql
admin ' OR 1= 1 -- 
```

Parola nici nu conteaza; inputul pe care il dau este:
- Username: `admin ' OR 1= 1 -- `
- Password: `e`



## Task 2 | Cross-Site Scripting


Pentru **alert**:

```html
<img src="nu-e-bn.png" onerror="alert("hello")">
```

in loc de:

```html
<src="images/simion-meme.png">
```




Pentru schimbare slogan, doar am pus un alt text in paragraf:

```html
<p>Don't vote!</p>
```

In loc de:
```html
<p>
You vote for Georgy Simion, da? He strong, like
        bear! Fight for people, for Romania, no corruption, only truth. Very
        good man! You give him vote! Make Romania great again, comrades!
</p>
```


## Task 4 | Server Reconnaissance


> Flag: **ISC{r3ad_th4_s0urce_Luke!}**.


**package.json** este fisirul despre care era vorba (pe care il au toate proiectele NodeJS).

So, intr-un tab din browser, am scris urmatorul request HTTP:
```
http://localhost:8080/package.json
```

Si am vazut ca server-ul nu ruleaza la **node.js** (cum m-as fi asteptat), ci la **server.js**:
```json
  ...
  "scripts": {
    "start": "node server.js"
  }
```

Inca un HTTP request pe `http://localhost:8080/server.js` si am cautat dupa **ISC{**.


## Task 5

Din cate vad, daca analizez unde se fac request-urile HTTP,
atunci cand dau **send** la un mesaj,
ma duce la urmatorul URL `http://localhost:8080/journal/post`,
si `http://localhost:8080/journal/delete?id=5` atunci cand dau **remove**.


Aceasta analiza se face din browser: **Click Dreapta -> Inspect -> Network**.
Eu cel mai bine m-am luat dupa coloane cu nume.

