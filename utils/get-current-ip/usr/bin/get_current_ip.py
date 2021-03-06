#!/usr/bin/env python3
"""
Get current public IP address and notify ourselves about it by email.
"""

import re
import time
import logging
import logging.handlers
import traceback
import threading
import requests
from var_waterpump import mailgun_apikey, mailgun_domain, mailgun_sender, mailgun_recipient

# Configure logging into syslog
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FORMAT = '%(pathname)s [%(levelname)s] %(lineno)s: %(message)s'
SYSLOG_HANDLER = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG_HANDLER.setFormatter(fmt=logging.Formatter(fmt=FORMAT))
LOGGER.addHandler(SYSLOG_HANDLER)

class IPMonitor: # pylint: disable=too-few-public-methods
    """
    Current purpose of this class is to define a class
    attribute `previous_public_ip`, so we can avoid using
    a global variable.
    """
    def __init__(self):
        self.previous_public_ip = ""

    def query_and_compare_public_ip(self):
        """
        Query currently active public IP assigned to the raspberry Pi and
        send an email to ourselves if it has changed.
        """
        current_public_ip = requests.get('https://api.ipify.org').text

        # Sometimes the api returns 'Application error', check if we have proper IP
        if re.match(r'\d+\.\d+\.\d+\.\d+', current_public_ip) and \
        current_public_ip != self.previous_public_ip:
            self.previous_public_ip = current_public_ip
            send_simple_message(current_public_ip)
            LOGGER.debug("Email successfully sent about newest public IP!")

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
    Instantiate an IPMonitor object, and start an infinite loop
    of the public IP comparing function. Sleep 60s inbetween
    queries.
    """
    ip_monitor = IPMonitor()
    while True:
        try:
            ip_monitor.query_and_compare_public_ip()
        except Exception:
            LOGGER.debug(traceback.print_exc())
        finally:
            time.sleep(60)

if __name__ == "__main__":
    try:
        threading.Thread(target=thread_function).start()
    except Exception: # pylint: disable=broad-except
        LOGGER.debug(traceback.print_exc())
