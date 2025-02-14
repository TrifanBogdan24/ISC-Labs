# Lab 11 - Privacy Technologies


*Cuprins*:
- [Lab 11 - Privacy Technologies](#lab-11---privacy-technologies)
  - [Task 0. Users](#task-0-users)
  - [Task 1. Pretty Good Privacy](#task-1-pretty-good-privacy)
    - [Generare chei pentru utilizatori](#generare-chei-pentru-utilizatori)
    - [Send **red**'s public key to **green**](#send-reds-public-key-to-green)
    - [Encrypt a file on **green**, send to **red** and decrypt](#encrypt-a-file-on-green-send-to-red-and-decrypt)
    - [Trust channel](#trust-channel)
  - [Task 2. Tor](#task-2-tor)
    - [Configurare Tor](#configurare-tor)
    - [DNS peste TCP (nu cred ca merge :()](#dns-peste-tcp-nu-cred-ca-merge-)
    - [Verificare adresa IP publica](#verificare-adresa-ip-publica)
    - [SSH (Local) Port Forwarding](#ssh-local-port-forwarding)
    - [Configurare Socks5 Proxy in Firefox](#configurare-socks5-proxy-in-firefox)

## Task 0. Users



```sh
sudo useradd -m -s /bin/bash red 
sudo useradd -m -s /bin/bash green 
sudo useradd -m -s /bin/bash blue 

sudo cp -r /home/student/.ssh /home/red/
sudo cp -r /home/student/.ssh /home/green/
sudo cp -r /home/student/.ssh /home/blue/

sudo chown -R red:red /home/red/.ssh
sudo chown -R green:green /home/green/.ssh
sudo chown -R blue:blue /home/blue/.ssh
```

Pasi:
1. Crearea utilizatorilor
2. Pentru a ma putea conecta cu SSH direct la userii nou creati,
  copiez directorul `~/.ssh/` din student la fiecare user in parte
3. Modific permisiunile pe directorul `~/.ssh/` pt fiecare user




## Task 1. Pretty Good Privacy

```sh
sudo apt update && sudo apt-get install -y rng-tools
```

```sh
sudo systemctl status rng-tools  # e pornit => TOTUL OK
```


### Generare chei pentru utilizatori


Generararea de chei cu `gpg` nu merge daca schimb user-ul si rulez comanda :(.

> For the next exercises,
> you will need to be **logged in as users red/green/blue via ssh**
> in order to generate the gpg key.



```sh
student in ~ at isc-vm …
➜ sudo su - red
red@isc-vm:~$ gpg --full-generate-key     # Nu merge, va da eroare :(
```


Astfel, trebuie sa ma conectez la useri prin SSH:


```sh
# TL;DR
ssh -J <moodle-username>@fep.grid.pub.ro blue@<IP-VM>
gpg --full-generate-key
```


```sh
❯ ssh -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>
red@isc-vm:~$ gpg --full-generate-key
Note that this key cannot be used for encryption.  You may want to use
the command "--edit-key" to generate a subkey for this purpose.
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid                      reduser <red@cs.pub.ro>
red@isc-vm:~$ exit
logout
```


```sh
❯ ssh -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>
green@isc-vm:~$ gpg --full-generate-key
Note that this key cannot be used for encryption.  You may want to use
the command "--edit-key" to generate a subkey for this purpose.
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      136E3F0C4558CE824270B63FAE8FA41610D6234C
uid                      green <green@cs.pub.ro>
green@isc-vm:~$ exit
logout
```



```sh
❯ ssh -J <moodle-username>@fep.grid.pub.ro blue@<IP-VM>
blue@isc-vm:~$ gpg --full-generate-key
Note that this key cannot be used for encryption.  You may want to use
the command "--edit-key" to generate a subkey for this purpose.
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      3953D4C3F5F87D64675B2A4983842759618CA7D4
uid                      blueuser <blue@cs.pub.ro>

blue@isc-vm:~$ exit
logout
```


### Send **red**'s public key to **green**

```sh
❯ ssh -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>
red@isc-vm:~$ gpg --export --armor red@cs.pub.ro > red-pub-key.asc
❯ scp -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>:red-pub-key.asc .        # Descarc (local) cheia publica de pe red
❯ scp -J <moodle-username>@fep.grid.pub.ro red-pub-key.asc green@<IP-VM>:~      # Uploadez cheia pe green
❯ ssh -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>
green@isc-vm:~$ cat red-pub-key.asc        # Double-check
green@isc-vm:~$ gpg --import red-pub-key.asc
green@isc-vm:~$ gpg --list-keys
```


```sh
green@isc-vm:~$ gpg --list-keys
/home/green/.gnupg/pubring.kbx
------------------------------
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      136E3F0C4558CE824270B63FAE8FA41610D6234C
uid           [ultimate] green <green@cs.pub.ro>

pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [ unknown] reduser <red@cs.pub.ro>
```



### Encrypt a file on **green**, send to **red** and decrypt
---

> Aici se ia o tzeapa!

Hai sa ne uitam la cheia publica a lui **red**:

```sh
green@isc-vm:~$ gpg --list-keys red@cs.pub.ro
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [ultimate] reduser <red@cs.pub.ro>
```

First of all, ar trebui sa o editam sa avem **incredere** in ea,
dar altceva e mai important acum :).

`[SC]`-ul ala nu e pus degeaba acolo, are o insemnate:
- `[S]` inseamna **signing capabilities**
- `[C]` inseamna **certification capabilites**

> Ca sa criptam date cu cheia publica, ar trebui sa vedem un `[E]` (de la **encryption**) pe acolo.

Si de vreme ce cheia publica se modifica (`edit`) doar impreuna cu cea privata, e numai buna de aruncat la gunoi :(.

```sh
green@isc-vm:~$ gpg --delete-key red@cs.pub.ro
gpg (GnuPG) 2.2.27; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.


pub  rsa4096/D13A27F88794CC12 2025-02-14 reduser <red@cs.pub.ro>

Delete this key from the keyring? (y/N) y
```

La fel si:

```sh
green@isc-vm:~$ rm red-pub-key.asc
```


Ma duc frumos inapoi pe **red** si dau `edit` la key-pair sa aiba si **encryption role**:

> `addkey` in promptul de **gpg** imi permite sa adaug noi roluri.

```sh
red@isc-vm:~$ gpg --list-keys 
/home/red/.gnupg/pubring.kbx
----------------------------
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [ultimate] reduser <red@cs.pub.ro>

red@isc-vm:~$ gpg --edit-key 5CF475123632668B9F639813D13A27F88794CC12
gpg (GnuPG) 2.2.27; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  rsa4096/D13A27F88794CC12
     created: 2025-02-14  expires: 2025-02-28  usage: SC  
     trust: ultimate      validity: ultimate
[ultimate] (1). reduser <red@cs.pub.ro>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
  (14) Existing key from card
Your selection? 6
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (3072) 4096
Requested keysize is 4096 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 2w
Key expires at Fri 28 Feb 2025 01:56:05 PM EET
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
 
sec  rsa4096/D13A27F88794CC12
     created: 2025-02-14  expires: 2025-02-28  usage: SC  
     trust: ultimate      validity: ultimate
ssb  rsa4096/9DCD7B5A3A5FE83F
     created: 2025-02-14  expires: 2025-02-28  usage: E   
[ultimate] (1). reduser <red@cs.pub.ro>

gpg>  save
red@isc-vm:~$ gpg --list-keys 
/home/red/.gnupg/pubring.kbx
----------------------------
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [ultimate] reduser <red@cs.pub.ro>
sub   rsa4096 2025-02-14 [E] [expires: 2025-02-28]

red@isc-vm:~$ 
```


Acum avem si `[E]` pe acolo.


```sh
# Export cheia publica
red@isc-vm:~$ gpg --export --armor red@cs.pub.ro > red-pub-key.asc

# Copiez cheia publica a lui red la green
❯ scp -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>:red-pub-key.asc green@<IP-VM>:~

# Connect to green
ssh -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>
green@isc-vm:~$ gpg --list-keys red@cs.pub.ro         # Acum va aparea ca poate sa si cripteze
green@isc-vm:~$ gpg --encrypt --recipient red@cs.pub.ro secret_file.txt
```


> La criptare
> - Nu merge sa redirectez continutul intr-un alt fisier :(
> - Va creea automat fisierul `secret_file.txt.gpg`

```sh
# Transfer de la green la red
❯ scp -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>:secret_file.txt.gpg red@<IP-VM>:~
❯ ssh -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>
red@isc-vm:~$ gpg --decrypt secret_file.txt.gpg 
gpg: encrypted with 4096-bit RSA key, ID 9DCD7B5A3A5FE83F, created 2025-02-14
      "reduser <red@cs.pub.ro>"
“text”
```

> La fel... la decriptare, nu merge sa redirectez contintul intr-un alt fisier :(.

> Also, la decriptare va cere si **passphrase**-ul (parola) pentru cheia privata.


### Trust channel


```sh
green@isc-vm:~$ gpg --sign-key red@cs.pub.ro      # Sign red's key
green@isc-vm:~$ gpg --list-keys 
/home/green/.gnupg/pubring.kbx
------------------------------
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      AA7511C6F6C7CEF4D45F999AC6F92EA541D95274
uid           [ultimate] green-user <green@cs.pub.ro>

pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [  full  ] reduser <red@cs.pub.ro>
sub   rsa4096 2025-02-14 [E] [expires: 2025-02-28]


green@isc-vm:~$ gpg --export --armor green@cs.pub.ro > green-pub-key.asc
green@isc-vm:~$ gpg --export --armor red@cs.pub.ro > red-pub-key.asc
❯ scp -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>:green-pub-key.asc blue@<IP-VM>:~
❯ scp -J <moodle-username>@fep.grid.pub.ro green@<IP-VM>:red-pub-key.asc blue@<IP-VM>:~
❯ ssh -J <moodle-username>@fep.grid.pub.ro blue@<IP-VM>
blue@isc-vm:~$ gpg --import green-pub-key.asc 
blue@isc-vm:~$ gpg --import red-pub-key.asc 
```
```sh
blue@isc-vm:~$ gpg --list-keys
/home/blue/.gnupg/pubring.kbx
-----------------------------
pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      3F02B56EAF1570792C194ABD0DB15707A553AA81
uid           [ultimate] blue-user <blue@cs.pub.ro>
sub   rsa4096 2025-02-14 [E] [expires: 2025-02-28]

pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      AA7511C6F6C7CEF4D45F999AC6F92EA541D95274
uid           [ unknown] green-user <green@cs.pub.ro>

pub   rsa4096 2025-02-14 [SC] [expires: 2025-02-28]
      5CF475123632668B9F639813D13A27F88794CC12
uid           [ unknown] reduser <red@cs.pub.ro>
sub   rsa4096 2025-02-14 [E] [expires: 2025-02-28]
```

```sh
❯ ssh -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>
red@isc-vm:~$ echo "Parola: 12345" > file.txt
red@isc-vm:~$ gpg --clearsign file.txt 
red@isc-vm:~$ ls -1
file.txt
file.txt.asc
❯ scp -J <moodle-username>@fep.grid.pub.ro red@<IP-VM>:file.txt.asc blue@<IP-VM>:~
❯ ssh -J <moodle-username>@fep.grid.pub.ro blue@<IP-VM>
```

```sh
blue@isc-vm:~$ cat file.txt.asc
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Parola: 12345
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEEXPR1EjYyZoufY5gT0Ton+IeUzBIFAmevTfMACgkQ0Ton+IeU
zBKILw/7Ba4qTHA9fKedfuYRoWthEHbvShskchmNwOhiKlq/0K2KaSI+qFdHvcU4
yzup84RCVavYk8YPtysTa3v1ncN3taCtS+AL18++WdMfsQ3btHXAcI/+YBTpXki8
b7+NtFgRhGGq8Em2iETTVMKo0ysr4QJVQgnU15ciV9brrCTePzLhBntZY3ha4bT1
nddKcg5dnl1yrx0WTWVj5ejz/lvr+3jh8Zkg715Yj5mxc7zQ99n7o28mr5dfocwy
HYqGqQ7q9jRCf97Kgqml6xCAhbZkRh7cFcVijlnRYxrm1qa7U1vONxlELU4Y1MGu
BNr/AZsMLxBEgrVWYBK+dY+y7mSsyu+DljwhlTbPndMuNN/djInpd0C3XpCBztKU
xskTkhp6C4fQwq32UZgljg+uh6rq5oxudVlk+4ypmkXkvhXWhxZXBovMLZ/GH+wA
Np3VZFBd0pf6mYzO3SA9wGur1yoVpLjbWbW50s7YErFpts78zzRVNE1gVaHQIAR8
2+i6IzssoC7dlf/fGQ1OCJuB/nDsRrF0tHOhwbX8ew1yz4w6EMt4EPJA4MqHHRoM
zRcvGL0i+sXCyvNvFuoasLJrkxWDEa2O8kdzhQJWdwCyXpyqHPyQ0dGvUfUHmFJM
tzhRXhMgc4II3cmYXXooDTmL9ZaA8XSceF/UNsNO4C7gPtbPTx0=
=Ge+c
-----END PGP SIGNATURE-----
```

```sh
blue@isc-vm:~$ gpg --edit-key green@cs.pub.ro
gpg (GnuPG) 2.2.27; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.


pub  rsa4096/C6F92EA541D95274
     created: 2025-02-14  expires: 2025-02-28  usage: SC  
     trust: unknown       validity: unknown
[ unknown] (1). green-user <green@cs.pub.ro>

gpg> trust
pub  rsa4096/C6F92EA541D95274
     created: 2025-02-14  expires: 2025-02-28  usage: SC  
     trust: unknown       validity: unknown
[ unknown] (1). green-user <green@cs.pub.ro>

Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

  1 = I don't know or won't say
  2 = I do NOT trust
  3 = I trust marginally
  4 = I trust fully
  5 = I trust ultimately
  m = back to the main menu

Your decision? 5
Do you really want to set this key to ultimate trust? (y/N) y

pub  rsa4096/C6F92EA541D95274
     created: 2025-02-14  expires: 2025-02-28  usage: SC  
     trust: ultimate      validity: unknown
[ unknown] (1). green-user <green@cs.pub.ro>
Please note that the shown key validity is not necessarily correct
unless you restart the program.

gpg> save
Key not changed so no update needed.
```



## Task 2. Tor


### Configurare Tor

```sh
sudo apt update && sudo apt install -y tor
```


Am cautat (`-i` **case insensitive**) textul "SOCKSPort 9050" in fisierul de configuratie TOR `/etc/tor/torrc`
si l-am deschis la linia unde se afla acest text pentru a o decomenta:


```sh
$ grep -i -n 'SOCKSPort 9050' /etc/tor/torrc
18:#SocksPort 9050 # Default: Bind to localhost:9050 for local connections.
```
```sh
sudo nano -l +18 /etc/tor/torrc
```



### DNS peste TCP (nu cred ca merge :()

Pentru a impune ca query-urile de DNS sa se faca peste TCP,
Chat GPT mi-a recomandat sa configurez **unbound** (nu stiu cat de bn este tho).


```sh
sudo apt install unbound -y
```

```sh
sudo nano /etc/unbound/unbound.conf.d/custom.conf
```
```
server:
    do-udp: no
    do-tcp: yes
```

```sh
sudo systemctl restart unbound
```

Comanda de verificare:

```sh
sudo systemctl status unbound
```

### Verificare adresa IP publica


```sh
sudo systemctl restart tor
```

```sh
sudo systemctl status tor
```

Pentru a afla adresa mea reala:
```sh
➜ curl ifconfig.me
141.85.150.35
```
Sau:
```sh
student in ~ at isc-vm …
➜ dig TXT +tcp +short o-o.myaddr.l.google.com @ns1.google.com | awk -F'"' '{ print $2 }'

141.85.150.35

```



Pentru a deschide un shell in **torsocks**:

```sh
torsocks bash
```


```sh
student in ~ at isc-vm …
➜ torsocks bash

student@isc-vm:~$ dig TXT +tcp +short o-o.myaddr.l.google.com @ns1.google.com | awk -F'"' '{ print $2}'
80.67.167.81

student@isc-vm:~$ curl https://check.torproject.org/api/ip
{"IsTor":true,"IP":"80.67.167.81"}
```



### SSH (Local) Port Forwarding


Pe calculatorul meu:


```sh
ssh -J <moodle-username>@fep.grid.pub.ro -L 9050:localhost:9050 -N -T student@<IP-VM>
```


| Optiune SSH | Descriere |
| :--- | :--- |
| `-L` | Creeaza un tunel **local** de **port forwarding** |
| `-N -T` | Impiedica SSH sa deschida un **shell** pe remote |


### Configurare Socks5 Proxy in Firefox

Daca scriu urmatorul URL in browser, <http://localhost:9050>,
o sa imi apara urmatorul text de eroare:

![img](./Images/img-01.png)

Pentru a folosi Tor Proxy,
1. Am deschis browser-ul local Firefox
2. Click pe meniul din coltul dreapta-sus
3. Select **Setting**
4. La search bar-ul unde scrie *Find in settings* am cautat **network**
5. La optiunea **Network Settings** -> click pe butonul **Settings**
6. Paste urmatoarea configuratie

![img](./Images/img-02.png)


Acum Tor functioneaza in browser-ul de Firefox.


Before and After:

<img src="./Images/img-03.jpeg" height=400px width=auto>
<img src="./Images/img-04.png" height=400px width=auto>
