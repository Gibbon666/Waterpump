#!/usr/bin/env python3
"""
Python script to automate taking photos with an Android phone.
"""

import os
import time
import logging
import logging.handlers
import traceback
import threading
from datetime import datetime
import urllib.request

# Configure logging into syslog
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FORMAT = '%(pathname)s [%(levelname)s] %(lineno)s: %(message)s'
SYSLOG_HANDLER = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG_HANDLER.setFormatter(fmt=logging.Formatter(fmt=FORMAT))
LOGGER.addHandler(SYSLOG_HANDLER)

def save_picture():
    """
    Save a picture by accessing the URL created by the IP Webcam app
    installed on an Android mobile phone.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H:%M:%S')
    photo_name = "/home/pi/Waterpump/photos/{}.jpg".format(timestamp)
    try:
        urllib.request.urlretrieve("http://192.168.1.3:8080/photo.jpg",
                                   photo_name)
    except (ConnectionRefusedError, urllib.error.URLError) as error:
        LOGGER.debug(error)
    finally:
        # Check if the photo created is an empty file
        if os.stat(photo_name).st_size == 0:
            LOGGER.debug("We've had an empty photo taken at {}".format(timestamp))
            os.unlink(photo_name)
        else:
            LOGGER.debug("Photo successfully taken: {}".format(photo_name))

def thread_function():
    """
    Create an infinite loop of the photo taking mechanism.
    """
    while True:
        try:
            save_picture()
        except Exception:
            LOGGER.debug(traceback.print_exc())
        finally:
            time.sleep(600)

if __name__ == "__main__":
    try:
        threading.Thread(target=thread_function).start()
    except Exception: # pylint: disable=broad-except
        LOGGER.debug(traceback.print_exc())
