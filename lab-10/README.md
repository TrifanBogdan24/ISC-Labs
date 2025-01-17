# Lab 10 - Tunnels. Remote Network Security

*Cuprins*:
- [Lab 10 - Tunnels. Remote Network Security](#lab-10---tunnels-remote-network-security)
  - [Task 2 | WireGuard](#task-2--wireguard)
    - [Metoda cu `iproute2`](#metoda-cu-iproute2)
    - [Metoda cu `wg-quick`](#metoda-cu-wg-quick)


## Task 2 | WireGuard


```sh
# Pe ambele statii
$ apt install -y wireguard
```


```sh
# IP: 10.9.1.169
$ wg genkey | tee wg-priv.key | wg pubkey | tee wg-pub.key
SJdQcHraRYr3+whwdGAWOMdqAHJBIoo8PVp8Vo+/tzI=
```


```sh
# IP: 10.9.1.224
$ wg genkey | tee wg-priv.key | wg pubkey | tee wg-pub.key
1yUrJzxG8ltzDfwbwUeH2vFWmUWErU9epcNa+/zepFI=
```

Pentru adresele de la capat de tunel, se va folosi subnetul **10.12.34.252/30**:
- **10.12.34.253/30** pt mine (10.9.1.169)
- **10.12.34.254/30** pt coleg (10.9.1.224)


### Metoda cu `iproute2`


```sh
# IP: 10.9.1.169
$ cat wg-priv.key
+DZ3OUvN3UW6uhWHg8U95sgZKPdexyiEkLApHguX+1k=

$ nano -l /etc/wireguard/wg-isc.conf
```
```sh
[Interface]
PrivateKey = +DZ3OUvN3UW6uhWHg8U95sgZKPdexyiEkLApHguX+1k=
ListenPort = 55820

[Peer]
PublicKey = 1yUrJzxG8ltzDfwbwUeH2vFWmUWErU9epcNa+/zepFI=
Endpoint = 10.9.1.224:55820
AllowedIPs = 10.12.34.252/30
```


```sh
# IP: 10.9.1.224
$ cat wg-priv.key     
MFujBC6C2GBB1U2pSqYo/s8xfmzpxCU9wY4RB16ol08=

$ nano -l /etc/wireguard/wg-isc.conf
```
```conf
[Interface]
PrivateKey = MFujBC6C2GBB1U2pSqYo/s8xfmzpxCU9wY4RB16ol08=
ListenPort = 55820

[Peer]
PublicKey = SJdQcHraRYr3+whwdGAWOMdqAHJBIoo8PVp8Vo+/tzI=
Endpoint = 10.9.1.169:55820
AllowedIPs = 10.12.34.252/30
```



Pornirea interfetelor de **WireGuard** folosind `iproute2`:

```sh
# IP: 10.9.1.169
$ ip link add wg-isc type wireguard
$ wg setconf wg-isc /etc/wireguard/wg-isc.conf
$ ip address add 10.12.34.253/30 dev wg-isc

# Interfata este initial DOWN, trebuie pornita
$ ip link set dev wg-isc up
```


```sh
# IP: 10.9.1.224
$ ip link add wg-isc type wireguard
$ wg setconf wg-isc /etc/wireguard/wg-isc.conf
$ ip address add 10.12.34.254/30 dev wg-isc

# Interfata este initial DOWN, trebuie pornita
$ ip link set dev wg-isc up
```


> Daca vreodata va trebui sa modific ceva in fisierele `.conf`,
> interfete trebuiesc oprite!


```sh
# Verificam IP-urile de pe toate interfetele
$ ip -br a s
```



```sh
# IP: 10.9.1.169
$ ping 10.12.34.254
```


```sh
# IP: 10.9.1.224
$ ping 10.12.34.253
```


```sh
# Show wireguard statistics
$ sudo wg
```



### Metoda cu `wg-quick`


Pe **10.9.1.169**:

```sh
$ wg-quick down wg-isc
[#] ip link delete dev wg-isc
```
```sh
$ nano -l /etc/wireguard/wg-isc.conf
```
```conf
[Interface]
Address = 10.12.34.253/30
PrivateKey = +DZ3OUvN3UW6uhWHg8U95sgZKPdexyiEkLApHguX+1k=
ListenPort = 55820

[Peer]
PublicKey = 1yUrJzxG8ltzDfwbwUeH2vFWmUWErU9epcNa+/zepFI=
Endpoint = 10.9.1.224:55820
AllowedIPs = 10.12.34.252/30
```
```sh
$ wg-quick up wg-isc  
[#] ip link add wg-isc type wireguard
[#] wg setconf wg-isc /dev/fd/63
[#] ip -4 address add 10.12.34.253/30 dev wg-isc
[#] ip link set mtu 1370 up dev wg-isc
```

Pe **10.9.1.224**:

```sh
$ wg-quick down wg-isc                        
[#] ip link delete dev wg-isc
```
```sh
$ nano -l /etc/wireguard/wg-isc.conf
```
```conf
[Interface]
Address = 10.12.34.254/30
PrivateKey = MFujBC6C2GBB1U2pSqYo/s8xfmzpxCU9wY4RB16ol08=
ListenPort = 55820

[Peer]
PublicKey = SJdQcHraRYr3+whwdGAWOMdqAHJBIoo8PVp8Vo+/tzI=
Endpoint = 10.9.1.169:55820
AllowedIPs = 10.12.34.252/30
```
```sh
$ wg-quick up wg-isc  
[#] ip link add wg-isc type wireguard
[#] wg setconf wg-isc /dev/fd/63
[#] ip -4 address add 10.12.34.254/30 dev wg-isc
[#] ip link set mtu 1370 up dev wg-isc
```


> `wg-quick` va rula automat comenzile cu `ip` :)

Iarasi, pentru a testa conectivitatea, rulam din nou `ping`-urile precedente.

