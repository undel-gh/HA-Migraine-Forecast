from collections import deque

class PressureTracker:
    def __init__(self):
        self.history = deque(maxlen=48)  # ~24h if 30min updates

    def add(self, value):
        if value is not None:
            self.history.append(value)

    def change(self, hours):
        steps = int(hours * 2)  # assuming 30min interval
        if len(self.history) < steps:
            return 0
        return self.history[-1] - self.history[-steps]
