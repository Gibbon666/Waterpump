import json

CREDS = json.load(open("/home/pi/Waterpump/creds.json", "r"))
mailgun_apikey = CREDS["mailgun-apikey"]
mailgun_domain = CREDS["mailgun-domain"]
mailgun_sender = CREDS["mailgun-sender"]
mailgun_recipient = CREDS["mailgun-recipient"]
