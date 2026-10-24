import importlib
import sys
import types
import unittest
import uuid
from unittest.mock import patch
from host.protocol import decode_packet
from firmware.micropython.lab_core import LabCore

class FakeBLE:
    def __init__(self):
        self.notifications = []
        self.advertisements = []
        self.fail = False
    def active(self, value): self.enabled = value
    def gap_advertise(self, interval, **kwargs): self.advertisements.append((interval, kwargs))
    def gatts_register_services(self, services): return ((12,),)
    def irq(self, handler): self.handler = handler
    def gatts_write(self, handle, value): self.value = value
    def gatts_notify(self, conn, handle, value):
        if self.fail: raise OSError("Disconnected")
        self.notifications.append((conn, value))

class BleTests(unittest.TestCase):
    def setUp(self):
        self.radio = FakeBLE()
        module = types.SimpleNamespace(BLE=lambda: self.radio, FLAG_READ=2, FLAG_NOTIFY=16,
                                       UUID=lambda s: uuid.UUID(s).bytes_le)
        with patch.dict(sys.modules, {"bluetooth": module}):
            name = "firmware.micropython.ble_instrument"
            sys.modules.pop(name, None)
            self.module = importlib.import_module(name)
            self.device = self.module.Instrument("PathwaysLab")
    def test_packet_end_to_end(self):
        lab = LabCore(); lab.update(50, 0, False)
        self.radio.handler(1, (7, 0, b""))
        self.device.publish(65536, 123, lab)
        sample = decode_packet(self.radio.notifications[0][1])
        self.assertEqual((sample.seq, sample.ms, sample.led), (0, 123, 1))
        self.assertLessEqual(len(self.radio.value), 20)
    def test_disconnect_advertises_again(self):
        self.radio.handler(1, (7, 0, b""))
        before = len(self.radio.advertisements)
        self.radio.handler(2, (7, 0, b""))
        self.assertFalse(self.device.connections)
        self.assertEqual(len(self.radio.advertisements), before + 1)
    def test_disconnect_race(self):
        self.radio.handler(1, (7, 0, b"")); self.radio.fail = True
        self.device.publish(0, 0, LabCore())
    def test_advertisement_fits(self):
        self.assertLessEqual(len(self.device.payload), 31)
        self.assertEqual(len(self.device.scan_response), 18)
