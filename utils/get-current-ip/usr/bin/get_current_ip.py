#!/usr/bin/env python3
"""
Get current public IP address and notify ourselves about it by email.
"""

import time
import threading
import requests
from var_waterpump import mailgun_apikey, mailgun_domain, mailgun_sender, mailgun_recipient

PREVIOUS_PUBLIC_IP = ""

def query_and_compare_public_ip():
    """
    Query currently active public IP assigned to the raspberry Pi and
    send an email to ourselves if it has changed.
    """
    global PREVIOUS_PUBLIC_IP
    current_public_ip = requests.get('https://api.ipify.org').text
    if current_public_ip != PREVIOUS_PUBLIC_IP:
        PREVIOUS_PUBLIC_IP = current_public_ip
        send_simple_message(current_public_ip)

def send_simple_message(public_ip):
    """
    Send an email to ourselves informing about given IP address.
    :param public_ip:   str, current public IP
    :return:            None
    """
    requests.post("https://api.mailgun.net/v3/{}/messages".format(mailgun_domain),
                  auth=("api", mailgun_apikey),
                  data={"from": mailgun_sender.format(mailgun_domain),
                       "to": mailgun_recipient,
                       "subject": "Raspberry Pi newest public IP",
                       "text": public_ip})

def thread_function():
    """
    Create an infinite loop of the public IP comparing function. Sleep 60s inbetween
    queries.
    """
    while True:
        query_and_compare_public_ip()
        time.sleep(60)

if __name__ == "__main__":
    try:
        x = threading.Thread(target=thread_function)
        x.start()
    except Exception as error:
        print(error)

