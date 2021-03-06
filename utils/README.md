# Utils created to provide useful information on the system

To build below Debian packages, use:

``` bash
dpkg-deb --build <package-name>
```

## Get current public IP

Get the current public IP and compare with the one stored in memory, if they don't match, send an email with the new one.
This way we are able to adjust our VNC connection and don't ever lose access to our device.

The systemd service [get-current-ip](get-current-ip) is run in a loop with 60s sleep time.

## Get notified about VNC users

Get notified about potential hackers trying to get in through VNC.

The systemd service [get-vnc-users](get-vnc-users) is run in a loop
with 0.5s sleep time, so we basically will get almost instant
notification about anybody trying to breach the system.

## Save a photo every x seconds

Take a photo with an Android phone connected at 192.168.1.3 to the local network
through the IP Webcam application.

The systemd service [save-photo](save-photo) is run in a loop
with 600s sleep time, so we are taking a photo every 10 minutes.