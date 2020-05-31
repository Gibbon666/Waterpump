# Waterpump

Raspberry Pi watering system using a peristaltic pump, a relay and a moisture sensor. Trying to mimic what was described here: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc

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

- Set up [fail2ban](docs/fail2ban_vnc_setup.md) service to ban hackers trying to get in through VNC (after 3 unsuccessful tries).

# Remote Monitoring

Several [utilities](utils) have been set up to provide useful information about the system.

# Current Crontabs and services:

## Crontabs

``` bash
@reboot cd /home/pi/Waterpump; sudo python3 waterpump_webserver.py
@reboot cd /home/pi/Waterpump; sudo python3 -c 'from waterpump_control import auto_water; auto_water()'
```

## Services

- get-current-ip
- get-vnc-users
