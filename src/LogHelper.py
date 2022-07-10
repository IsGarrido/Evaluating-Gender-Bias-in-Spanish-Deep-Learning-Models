class LogHelper:

    log = ''

    def log_print(self, t):
        self.log += (t + "\n")
        print(t)

    def get_log(self):
        xlog = self.log
        self.log = ''
        return xlog