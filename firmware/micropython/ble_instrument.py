"""Read/notify instrument. 12-byte packets fit the default ATT payload."""
import struct
import bluetooth

SERVICE_UUID = "56f90001-20bb-4c54-8b27-48a5e3351a4e"
DATA_UUID = "56f90002-20bb-4c54-8b27-48a5e3351a4e"

class Instrument:
    def __init__(self, name="PathwaysLab"):
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.gap_advertise(None)
        service = (bluetooth.UUID(SERVICE_UUID), (
            (bluetooth.UUID(DATA_UUID), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),))
        ((self.handle,),) = self.ble.gatts_register_services((service,))
        self.connections = set()
        self.ble.irq(self._irq)
        short_name = name.encode()[:26]
        self.payload = b"\x02\x01\x06" + bytes((len(short_name) + 1, 9)) + short_name
        self.scan_response = b"\x11\x07" + bytes(bluetooth.UUID(SERVICE_UUID))
        self.advertise()

    def advertise(self):
        self.ble.gap_advertise(250000, adv_data=self.payload,
                               resp_data=self.scan_response)

    def _irq(self, event, data):
        if event == 1:  # central connected
            self.connections.add(data[0])
        elif event == 2:  # central disconnected
            self.connections.discard(data[0])
            self.advertise()

    def publish(self, sequence, ms, lab):
        flags = int(lab.led) | (int(lab.button) << 1) | (int(lab.running) << 2)
        data = struct.pack("<BBHIHH", 1, flags, sequence & 65535,
                           ms & 0xffffffff, lab.input, lab.period)
        self.ble.gatts_write(self.handle, data)
        for connection in tuple(self.connections):
            try:
                self.ble.gatts_notify(connection, self.handle, data)
            except OSError:
                # A peer may disconnect between snapshot and notify; IRQ owns cleanup.
                pass
