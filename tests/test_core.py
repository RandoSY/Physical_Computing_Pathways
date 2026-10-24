import unittest
from firmware.micropython.lab_core import LabCore

class CoreTests(unittest.TestCase):
    def test_period_endpoints(self):
        lab = LabCore()
        for value, period in ((0, 100), (65535, 2000), (32768, 1050)):
            lab.update(0, value, False)
            self.assertEqual(lab.period, period)

    def test_blink_and_pause(self):
        lab = LabCore()
        lab.update(49, 0, False); self.assertFalse(lab.led)
        lab.update(50, 0, False); self.assertTrue(lab.led)
        lab.update(51, 0, True)
        lab.update(75, 0, True); self.assertTrue(lab.running)
        lab.update(76, 0, True); self.assertFalse(lab.running)
        self.assertFalse(lab.led)
        lab.update(10000, 0, True); self.assertFalse(lab.running)
        lab.update(10001, 0, False); lab.update(10026, 0, False)
        lab.update(10027, 0, True); lab.update(10052, 0, True)
        self.assertTrue(lab.running)

    def test_bounce_does_not_pause(self):
        lab = LabCore()
        for ms, pressed in ((1, True), (5, False), (10, True), (20, False), (60, False)):
            lab.update(ms, 0, pressed)
        self.assertTrue(lab.running)

    def test_ticks_wrap(self):
        diff = lambda a, b: ((a - b + 512) % 1024) - 512
        lab = LabCore(diff)
        lab.edge = 1000
        lab.update(26, 0, False)
        self.assertTrue(lab.led)
        lab.update(1010, 0, True)
        lab.update(11, 0, True)
        self.assertFalse(lab.running)
