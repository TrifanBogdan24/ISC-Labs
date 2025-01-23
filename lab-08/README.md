# Lab 08 - Network Security


## Task1 | Port Scanning

### Discover Devices on the Network

- `-sn`: ping scan pentru `nmap`


```sh
$ nmap -sn <IP-retea>/<mask> 
$ nmap -sn 10.9.0.0/16
```

OpenStack's network prefix: 10.9._._/16

### Scan a Machine for Open Ports on TCP/UDP

```sh
# IP Coleg: 10.9.2.212
$ nc -lp $(((RANDOM % 2001) + 1000))
```

```sh
# Scanare port range
$ nmap -p 1000-3000 10.9.2.212
```

Flag-ul `-p` specifica un interval de porturi.


### OS/Version scans


```sh
$ nmap -O 10.9.2.212
```

`-O` flag enable OS detection.



```sh
$ nmap -sV -Pn 10.9.2.212
```

- `-sV`: determina info despre servicii/versiuni
- `-Pn`: trateaza host-ul ca fiind online


## Task 2 | iptables


### Secure Your VM from Unwanted SSH/HTTP Traffic


**STEP 1**: Access Your Colleague’s VM and Observe Traffic


Din nu stiu ce motive, conexiunea prin ftp/curl/ssh nu merge catre colegul.

A trebuit sa:
1. Generez o pereche de chei SSH pe VM-ul meu
2. A trebuit sa ii dau coleguluui cheia mea privata (ca nici `ssh-copy-id` nu merge)  
    si sa o adauge manual la `~/.ssh/authorized_keys`

Eu:

```sh
# Comanda generare chei SSH
ssh-keygen -t ed25519 -f ~/.ssh/coleg -N ""
```

Colegul:

```sh
# sau vim
nano -l ~/.ssh/authorized_keys
```


```sh
# Conectare
ssh -i ~/.ssh/coleg student@<IP-Coleg>
```


**STEP 2**: Monitor Incoming Traffic with tcpdump


```sh
# Un fel de tcdump (WireShark in CLI)
root@host:~# apt install -y tshark
```

```sh
root@host:~# tshark -i eth0 | grep 'SSH'
Running as user "root" and group "root". This could be dangerous.
Capturing on 'eth0'
 ** (tshark:2512) 17:20:29.419217 [Main MESSAGE] -- Capture started.
 ** (tshark:2512) 17:20:29.419771 [Main MESSAGE] -- File: "/tmp/wireshark_eth06HOW02.pcapng"
34     1 0.000000000     10.9.5.9 → 141.85.150.247 SSH 118 Server: Encrypted packet (len=52)
    2 0.000047777     10.9.5.9 → 141.85.150.247 SSH 118 Server: Encrypted packet (len=52)
    3 0.000131582     10.9.5.9 → 141.85.150.247 SSH 166 Server: Encrypted packet (len=100)
    4 0.000184417     10.9.5.9 → 141.85.150.247 SSH 190 Server: Encrypted packet (len=124)
    9 0.754664756     10.9.5.9 → 141.85.150.247 SSH 110 Server: Encrypted packet (len=44)
```


> IP-ul pentru fep.grid este **141.85.150.247**.

**STEP 3**: Block Unwanted SSH and HTTP Traffic



```sh
# IP fep: 141.85.150.247
root@host:~# iptables -A INPUT -p tcp -s <IP-fep> -m multiport --dports 22,80 -j ACCEPT
root@host:~# iptables -A INPUT -p tcp -s <IP-coleg> -m multiport --dports 22,80 -j ACCEPT
root@host:~# iptables -A INPUT -p tcp -m multiport --dports 22,80 -j REJECT
```





## Task 3 | Workstation Firewall


```sh
# Remove any existing rules from all chains
iptables --flush
 
# Allow traffic on the loopback interface
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow SSH traffic
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
 
# Accept any related or established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
 
# Set the default policy to drop
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
 
# Outbound DNS lookups
iptables -A OUTPUT -o ens3 -p udp -m udp --dport 53 -j ACCEPT
 
# Allow outbound SSH
iptables -A OUTPUT -o ens3 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
 
# Outbound PING requests
iptables -A OUTPUT -o ens3 -p icmp -j ACCEPT
 
# Outbound Network Time Protocol (NTP) requests
iptables -A OUTPUT -o ens3 -p udp --dport 123 --sport 123 -j ACCEPT
 
# Outbound HTTP and HTTPS
iptables -A OUTPUT -i ens3 -p tcp -m tcp --dport 80 -m state --state NEW -j ACCEPT
iptables -A OUTPUT -i ens3 -p tcp -m tcp --dport 443 -m state --state NEW -j ACCEPT
```



## Task 4 | DNS Blocking


```sh
$ iptables -A INPUT -p udp --dport 53 -m string --hex-string "|08 66 61 63 65 62 6F 6F 6B 03 63 6F 6D 00|" --algo bm -j REJECT
$ iptables -A INPUT -p tcp --dport 53 -m string --hex-string "|08 66 61 63 65 62 6F 6F 6B 03 63 6F 6D 00|" --algo bm -j REJECT
```


`08 66 61 63 65 62 6F 6F 6B 03 63 6F 6D 00`: encodarea pentru *facebook.com*

- `08` = Length of "facebook"
- `66 61 63 65 62 6F 6F 6B` = ASCII for "facebook"
- `03` = Length of "com"
- `63 6F 6D` = ASCII for "com"
- `00` = Null terminator




Before `iptables`:


```sh
➜ ping -c 1 facebook.com
PING facebook.com (185.60.218.35) 56(84) bytes of data.
64 bytes from edge-star-mini-shv-01-otp1.facebook.com (185.60.218.35): icmp_seq=1 ttl=55 time=1.47 ms

--- facebook.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.473/1.473/1.473/0.000 ms
```

After `iptables`:

```sh
➜ ping facebook.com
ping: facebook.com: Temporary failure in name resolution
```