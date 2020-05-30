# Waterpump

Raspberry Pi watering system using a peristaltic pump, a relay and a moisture sensor. Trying to mimic what was described here: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc

# Remote Monitoring

I've configured port forwarding and set up an SMTP service which will send me daily emails about the current public IP address, so I can monitor the status of the watering system from wherever I want.

# Current Crontabs

``` bash
@reboot cd /home/pi/Waterpump; sudo python3 waterpump_webserver.py
@reboot cd /home/pi/Waterpump; sudo python3 -c 'from waterpump_control import auto_water; auto_water()'
0 9 * * * cd /home/pi/Waterpump; PYTHONPATH=$PYTHONPATH:/home/pi/Waterpump sudo python3 utils/get_current_ip.py
#* * * * * cd /home/pi/Waterpump; sudo python3 utils/get_vnc_users.py --> Running now as a systemd service `get-vnc-users`
```
