#!/usr/bin/env python3
"""
This python script will serve as a base for a systemd service to
be run on the raspberry pi to check for intruders on the VNC port.
"""

import os
import re
import time
import datetime
import threading
import requests
from var_waterpump import mailgun_apikey, mailgun_domain, mailgun_sender, mailgun_recipient

def check_potential_hackers():
    """
    1. Check currently active VNC users with `ss sport = :5900` bash command
    2. If there were active connections (which could mean potential hackers)
       save their IP to a variable
    3. Check if we already have that IP in logs/vnc_users.log,
       if not, then save it in the same file (in a new line)
    4. Finally send an email to us for every (potential) hacker about
       their IP address.
    """
    active_vnc_users = os.popen("ss sport = :5900").readlines()
    split_output = str(active_vnc_users[1:]).split(' ')
    found_ips = [re.findall(r'\d+.\d+.\d+.\d+:\d+', x) for x in split_output]
    ips_filtered = [x for x in found_ips if x != [] and not x[0].startswith('192.168')]

    with open('/home/pi/Waterpump/logs/vnc_users.log', 'a') as f_append:
        with open('/home/pi/Waterpump/logs/vnc_users.log', 'r') as f_read:
            try:
                vnc_log = f_read.readlines()
                vnc_log_sanitized = [x.split('\n')[0] for x in vnc_log]
            except FileNotFoundError:
                vnc_log_sanitized = ['']

            for active_ip in ips_filtered:
                if not any(active_ip[0] in old_ips for old_ips in vnc_log_sanitized):
                    vnc_connection_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    f_append.write(vnc_connection_at + ' from ' + active_ip[0] + '\n')

                    # Notify ourselves about a possible intruder.
                    requests.post(
                        "https://api.mailgun.net/v3/{}/messages".format(mailgun_domain),
                        auth=("api", mailgun_apikey),
                        data={"from": mailgun_sender.format(mailgun_domain),
                              "to": mailgun_recipient,
                              "subject": "New VNC user detected",
                              "text": "New VNC user from: {}".format(active_ip[0])})

                # else: intruder IP already known, do nothing

def thread_function():
    """
    Create an infinite loop of the VNC intruder monitor function
    """
    while True:
        check_potential_hackers()
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        x = threading.Thread(target=thread_function)
        x.start()
    except Exception as error:
        print(error)
