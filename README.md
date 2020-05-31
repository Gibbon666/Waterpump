# Waterpump

Raspberry Pi watering system using a peristaltic pump, a relay and a moisture sensor. Trying to mimic what was described at [https://www.hackster.io](https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc), enchanced with some security measures.

# Port forwarding & Firewall

Some services have been enabled to be reachable from outside the internet.

## SSH:

- Port forwarding & firewall rule to allow traffic on port 22.

- /etc/ssh/sshd_config settings modified:

```
AllowTcpForwarding yes
```

## VNC

- Port forwarding & firewall rule to allow traffic on port 5900.

# Fail2ban

Set up [fail2ban](docs/) service to:

1. ban hackers trying to get in through VNC (after 3 unsuccessful tries).

2. ban hackers trying to get in through SSH (after 3 unsuccessful tries).

# Remote Monitoring

Several [utilities](utils) have been set up to provide useful information about the system.

# Current Crontabs and services:

## Crontabs

``` bash
@reboot cd /home/pi/Waterpump; sudo python3 waterpump_webserver.py
@reboot cd /home/pi/Waterpump; sudo python3 -c 'from waterpump_control import auto_water; auto_water()'
```

## Services

Below services are currently installed on the Raspberry Pi as a Debian package:

- get-current-ip
- get-vnc-users
