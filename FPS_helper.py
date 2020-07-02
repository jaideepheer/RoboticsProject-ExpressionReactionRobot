import time
import collections
class time_marker:
    def __init__(self, history_buffer_size=256):
        self.marker = time.time_ns()
        self.max_ellapsed = 0
        self.ellapse_history = collections.deque()
        self.history_buffer_size = history_buffer_size
    def average_ellapsed_ns(self):
        if(len(self.ellapse_history)>0):
            return sum(self.ellapse_history)/len(self.ellapse_history)
        else:
            return 0
    def average_ellapsed_ms(self):
        return self.average_ellapsed_ns()/(10**6)
    def mark(self):
        self.marker = time.time_ns()
    def ellapsed_ns(self):
        ellapsed = time.time_ns()-self.marker
        if(ellapsed>self.max_ellapsed):
            self.max_ellapsed = ellapsed
        if(len(self.ellapse_history)==self.history_buffer_size):
            self.ellapse_history.popleft()
        self.ellapse_history.append(ellapsed)
        return ellapsed
    def ellapsed_ms(self):
        return self.ellapsed_ns()/(10**6)
    def ellapsed_sec(self):
        return self.ellapsed_ns()/(10**9)
    def max_ellapsed_ns(self):
        return self.max_ellapsed
    def max_ellapsed_ms(self):
        return self.max_ellapsed_ns()/(10**6)