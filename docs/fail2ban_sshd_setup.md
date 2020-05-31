# Fail2ban service for SSHD

Settings created based the guide found at [https://www.booleanworld.com](https://www.booleanworld.com/protecting-ssh-fail2ban/).

## 1. If /etc/fail2ban/jail.local is not existing, create it by either copying jail.conf or by creating an empty file.

## 2. Copy and paste below stuff at [sshd] block of /etc/fail2ban/jail.local

``` bash
[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s
action = %(action_)s
#banaction = iptables-multiport
maxretry = 3
findtime = 43200
bantime = -1
```