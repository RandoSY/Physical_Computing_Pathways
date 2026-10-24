"""Strict decoder shared by USB serial, BLE, and the offline simulator."""
import struct
from dataclasses import dataclass

SERVICE_UUID = "56f90001-20bb-4c54-8b27-48a5e3351a4e"
DATA_UUID = "56f90002-20bb-4c54-8b27-48a5e3351a4e"
FIELDS = ("seq", "ms", "input_u16", "led", "button", "running", "period_ms")
PACKET = struct.Struct("<BBHIHH")

@dataclass(frozen=True)
class Sample:
    seq: int
    ms: int
    input_u16: int
    led: int
    button: int
    running: int
    period_ms: int

    def __post_init__(self):
        limits = (65535, 0xffffffff, 65535, 1, 1, 1, 2000)
        for name, limit in zip(FIELDS, limits):
            value = getattr(self, name)
            if type(value) is not int or not 0 <= value <= limit:
                raise ValueError("Invalid " + name)
        if self.period_ms < 100:
            raise ValueError("period_ms must be 100..2000")

    def row(self):
        return tuple(getattr(self, name) for name in FIELDS)

def decode_line(line):
    if isinstance(line, bytes):
        line = line.decode("ascii")
    fields = line.strip().split(",")
    if len(fields) != len(FIELDS):
        raise ValueError("Expected seven comma-separated integers")
    return Sample(*(int(value) for value in fields))

def decode_packet(data):
    if len(data) != PACKET.size:
        raise ValueError("Expected 12-byte BLE packet")
    version, flags, seq, ms, value, period = PACKET.unpack(data)
    if version != 1 or flags & ~7:
        raise ValueError("Unsupported protocol version/flags")
    return Sample(seq, ms, value, flags & 1, (flags >> 1) & 1,
                  (flags >> 2) & 1, period)
