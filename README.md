# Waterpump

Raspberry Pi watering system using a peristaltic pump, a relay and a moisture sensor. Trying to mimic what was described here: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc

# Remote Monitoring

Several [utilities](utils) have been set up to provide useful information about the system.

# Fail2ban 

Set up [fail2ban](docs/fail2ban_vnc_setup.md) service to ban hackers trying to get in through VNC.

# Current Crontabs and services:

## Crontabs

``` bash
@reboot cd /home/pi/Waterpump; sudo python3 waterpump_webserver.py
@reboot cd /home/pi/Waterpump; sudo python3 -c 'from waterpump_control import auto_water; auto_water()'
0 9 * * * cd /home/pi/Waterpump; PYTHONPATH=$PYTHONPATH:/home/pi/Waterpump sudo python3 utils/get_current_ip.py
```

## Services

get-vnc-users
