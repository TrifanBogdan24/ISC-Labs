# Lab 01 - Introduction

*Cuprins*:
- [Lab 01 - Introduction](#lab-01---introduction)
  - [Task 01 | Decode 'til You Drop](#task-01--decode-til-you-drop)
  - [Task 02 | Zip it good](#task-02--zip-it-good)
  - [Task 03 | Find the impostor](#task-03--find-the-impostor)

## Task 01 | Decode 'til You Drop


> Flag obtinut: **ISC{44e1da16-40a7-4439-bac0-ceb5b20ae481}**


Am urmatorul string codificat de mai multe ori in **base64**:
```
VmxSR1lWUXhTa2hXYWxwV1ZrVkthRlpyVm1GamJHUlhWV3RhVG1FemFGWldWbWhyVjJ4YVNGUnFRbFZoTVVwVFdsZHpOVlpGTVZoaVJuQlhUVVJGZWxaRldtdFVNa3BIWWtoR1YySlhlRTlaVjNSTFlqRmtjMVZzU2s5U1ZFWmFWRlZSZDFCUlBUMD0=
```


Cel mai usor am aflat flag-ul decodand iterativ intr-un pipeline din **shell**:


```sh
$ echo <string> | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d
```


Sau... metoda muncitoreasca:

```py
#!/usr/bin/env python3

import base64

encoded_text = b'....'

# Solution:
flag = base64.b64decode(encoded_text).decode("utf-8")
flag = base64.b64decode(flag).decode("utf-8")
flag = base64.b64decode(flag).decode("utf-8")
flag = base64.b64decode(flag).decode("utf-8")
flag = base64.b64decode(flag).decode("utf-8")


print("Final decoded text:", flag)
```



## Task 02 | Zip it good

> Flag obtinut: **ISC{991e7f7d-ac8e-4570-a012-8fb9314b4380}**

Fisierul **passwords.txt** contine o lista cu posibile parole cu care arhiva a fost critata.


Varianta in **bash**


```sh
# Sintaxa sh dezarhivare cu parola
$ unzip -P 'parola' archive.zip
```


```sh
#!/usr/bin/env bash

for passwd in $(cat passwords.txt) ; do
    unzip -P "$passwd" crack_me.zip
    exit_code=$?
    if [[ $exit_code == 0 ]] ; then
        echo "Yuppi! Password found: $passwd"
        exit 0
    fi
done
```



Varianta in **python**:

```py

def crack_zip(zip_file, passwords_file):
    with zipfile.ZipFile(zip_file) as zf:
        with open(passwords_file, 'r') as pf:
            for line in pf:
                password = line.strip()
                try:
                    zf.extractall(pwd=bytes(password, 'utf-8'))
                    print(f"Yuppi! Password found: {password}")
                    return 0
                except:
                    continue
            print("[ERROR] The 'passwords.txt' does NOT contain a valid password!", file=sys.stderr)
            return 1 
    return None


if __name__ == '__main__':
    crack_zip('crack_me.zip', 'passwords.txt')
```


> Parola este **sunshine**.


## Task 03 | Find the impostor

> Flag obtinut: **ISC{manual-pages-are-your-friends}**


```sh
$ find inhere/ -type f -readable -size 987c ! -executable

$ cat $(find inhere/ -type f -readable -size 987c ! -executable)
```