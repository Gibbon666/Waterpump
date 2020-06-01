#!/usr/bin/env python3
"""
Python script to automate taking photos with an Android phone.
"""

import time
import threading
from datetime import datetime
import urllib.request

def save_picture():
    """
    Save a picture by accessing the URL created by the IP Webcam app
    installed on an Android mobile phone.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H:%M:%S')
    try:
        urllib.request.urlretrieve("http://192.168.1.3:8080/photo.jpg",
                                   "/home/pi/Waterpump/photos/{}.jpg".format(timestamp))
    except (ConnectionRefusedError, urllib.error.URLError) as error:
        print(error)

def thread_function():
    """
    Create an infinite loop of the photo taking mechanism.
    """
    while True:
        save_picture()
        time.sleep(600)

if __name__ == "__main__":
    try:
        threading.Thread(target=thread_function).start()
    except Exception as error: # pylint: disable=broad-except
        print(error)
