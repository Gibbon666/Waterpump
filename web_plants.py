from flask import Flask, render_template, redirect, url_for, request
import psutil
import datetime
import water
import os
import re

app = Flask(__name__)

def template(title="HELLO!", text="", pump_status="", full_log=""):
    now = datetime.datetime.now()
    timeString = now
    templateData = {
        'title' : title,
        'time' : timeString,
        'text' : text,
        'pump_status' : pump_status,
        'full_log': full_log
        }
    return templateData

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    try:
        with open('/home/pi/Waterpump/watering_log.txt', 'r') as f:
            full_log = f.readlines()
        parsed_for = [line.split('for ') for line in full_log if len(line) > 1]
        parsed_for_last = [x[-1] for x in parsed_for]
        parsed_numbers = [re.findall(r'\d+', x) for x in parsed_for_last]
        total = 0
        number_of_watering = len(parsed_numbers)
        for number in parsed_numbers:
            total += int(number[0])
        templateData = template(text = water.get_last_watered(), 
                                pump_status="Total watering time: {} seconds after {} occasions.".format(total, number_of_watering))
        return render_template('main.html', **templateData)
    except:
        templateData = template(text = water.get_last_watered())
        return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    moisture_status, pump_status = water.get_status()
    message = ""
    if (moisture_status == 1):
        message = "I'm quite possibly just malfunctioning, but it is also possible that the soil is quite dry."
    else:
        message = "My soil is quite wet, hence this message."

    templateData = template(text=message, pump_status=pump_status)
    return render_template('main.html', **templateData)

@app.route("/full_log")
def show_full_log():
    try:
        with open('watering_log.txt', 'r') as f:
            full_log = f.readlines()
        html_compatible_log = ''
        for line in full_log:
            html_compatible_log += line + '<br>'    
        templateData = template(full_log=html_compatible_log)
        return render_template('main.html', **templateData)
    except:
        templateData = template(text="No logs so far.")
        return render_template('main.html', **templateData)

@app.route("/water",  methods=['GET', 'POST'])
def water_for_specific_number_of_seconds():
    try:
        number_of_seconds = int(request.form['pump_time'])
        water.pump_on(number_of_seconds=number_of_seconds, automatically=0)
        templateData = template(text = "Watered Once for {} seconds.".format(number_of_seconds))
        return render_template('main.html', **templateData)
    except Exception as e:
        templateData = template(text = "Invalid input, skipping pump initiation.")
        return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    running = False
    for process in psutil.process_iter():
        try:
            if process.cmdline()[1] == 'auto_water.py':
                running = True
        except:
            pass
    if not running:
        os.system("python3 auto_water.py&")
