import time
class time_marker:
    def __init__(self):
        self.marker = time.time_ns()
    def mark(self):
        self.__init__()
    def ellapsed_ns(self):
        return time.time_ns()-self.marker
    def ellapsed_sec(self):
        return self.ellapsed_ns()/10**9