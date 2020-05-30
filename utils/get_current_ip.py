#!/usr/bin/env python3
"""
Get current public IP address and notify ourselves about it with email.
"""

import requests
from var_waterpump import mailgun_apikey, mailgun_domain, mailgun_sender, mailgun_recipient

def send_simple_message():
    """
    Query currently active public IP assigned to the raspberry Pi and
    send an email to ourselves.
    """
    public_ip = requests.get('https://api.ipify.org').text
    return requests.post("https://api.mailgun.net/v3/{}/messages".format(mailgun_domain),
                         auth=("api", mailgun_apikey),
                         data={"from": mailgun_sender.format(mailgun_domain),
                               "to": mailgun_recipient,
                               "subject": "Raspberry Pi newest public IP",
                               "text": public_ip})

if __name__ == "__main__":
    send_simple_message()
