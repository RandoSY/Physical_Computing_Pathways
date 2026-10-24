"""Pure Python state machine; pass time.ticks_diff on MicroPython."""

class LabCore:
    def __init__(self, diff=lambda a, b: a - b):
        self.diff = diff
        self.led = False
        self.running = True
        self.button = False
        self.candidate = False
        self.changed = self.edge = 0
        self.input = 0
        self.period = 100

    def update(self, now, value, pressed):
        self.input = max(0, min(65535, int(value)))
        self.period = 100 + self.input * 1900 // 65535
        if pressed != self.candidate:
            self.candidate, self.changed = pressed, now
        if self.candidate != self.button and self.diff(now, self.changed) >= 25:
            self.button = self.candidate
            if self.button:
                self.running = not self.running
                self.led, self.edge = False, now
        if not self.running:
            self.led = False
        elif self.diff(now, self.edge) >= self.period // 2:
            self.led, self.edge = not self.led, now
