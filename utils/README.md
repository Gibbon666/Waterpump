# Utils created to provide useful information on the system

## Get current public IP

We get current public IP of the Raspberry Pi by running [get_current_ip.py](get_current_ip.py) every day with a crontab.

This way we are able to adjust our VNC connection and don't ever lose access to our device.

## Get notified about VNC users

We are getting notified about potential hackers trying to get in through VNC through a script placed on the Raspberry Pi as a systemd service. 

[get-vnc-users](get-vnc-users) itself is a Debian package that we need to install on the device. It will then create the service for us and we get instant notification in email about anybody who has e.g. brought up the VNC login page.