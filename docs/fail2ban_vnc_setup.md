# Fail2ban service for VNC

## 1. If /etc/fail2ban/jail.local is not existing, create it by either copying jail.conf or by creating an empty file.

## 2. Copy and paste below stuff at the end of /etc/fail2ban/jail.local

``` bash
[vncserver]
enabled = true
filter = vncserver
port = 5900
action = %(action_)s
#banaction = iptables-multiport
bantime = -1
maxretry = 3
logpath = /var/log/syslog
```

## 3. Create /etc/fail2ban/filter.d/vncserver.conf with below content:

``` bash
# Fail2Ban filter for RealVNC auth failures
[INCLUDES]
before = common.conf

[Definition]
failregex = ^.+vncserver-x11\[\d+\,root\](:) (Connections:) (disconnected:).+?<HOST>(::)\d+ \(TCP\) \(\[(AuthFailure)\] (Either the username was not recognised\, or the password was incorrect\))\s*$

ignoreregex =
```

## 4. Above regex should work for below texts in /var/log/syslog:

```
Sep 11 17:25:05 raspberrypi vncserver-x11[445,root]: Connections: disconnected: 18x.23x.17x.14x::4722 (TCP) ([AuthFailure] Either the username was not recognised, or the password was incorrect)
```

## 5. Useful commands:

``` bash
# Adding IP to ban manually:
sudo fail2ban-client -vvv set vncserver banip 34.76.210.152

# Checking currently banned IPs:
sudo fail2ban-client status vncserver

# Checking if our regex works for current syslog content:
sudo fail2ban-regex /var/log/syslog vncserver.conf
```