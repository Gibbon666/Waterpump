# External module imp
import RPi.GPIO as GPIO
import schedule
import datetime
import time

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("watering_log.txt", "r")
        return f.read().splitlines()[-1]
    except:
        return "NEVER!"
      
def get_status(water_sensor_pin=17, pump_pin=14):
    GPIO.setup(water_sensor_pin, GPIO.IN)
    GPIO.setup(pump_pin, GPIO.OUT)
    return [GPIO.input(water_sensor_pin), 'Pump currently on' if not GPIO.input(pump_pin) else 'Pump currently off']

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    
def auto_water(pump_pin = 14):
    schedule.every().minute.do(pump_on)
    while True:
        schedule.run_pending()

def pump_on(pump_pin=14, number_of_seconds=20, automatically=1):
    init_output(pump_pin)
    pump_initiated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    trigger = "automatically" if automatically else "by Daniel Baranyai"
    f = open("watering_log.txt", "a+")
    f.write("{} Pump started {} for {} seconds\n".format(pump_initiated_at, trigger, number_of_seconds))
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(number_of_seconds)
    GPIO.output(pump_pin, GPIO.HIGH)