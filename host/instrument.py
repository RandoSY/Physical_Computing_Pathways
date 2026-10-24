"""Run from repository root: python -m host.instrument demo --seconds 10."""
import argparse
import asyncio
import csv
import math
import sys
import time
from contextlib import contextmanager
from .protocol import FIELDS, DATA_UUID, Sample, decode_line, decode_packet

@contextmanager
def output(path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDS)
        count = 0
        def emit(sample):
            nonlocal count
            count += 1
            writer.writerow(sample.row())
            handle.flush()
            level = sample.input_u16 * 25 // 65535
            gauge = "=" * level + " " * (25 - level)
            print("\r[{}] input={:5d} period={:4d}ms LED={} RUN={} seq={:5d}".format(
                gauge, sample.input_u16, sample.period_ms, sample.led,
                sample.running, sample.seq), end="", flush=True)
        try:
            yield emit
            if not count:
                raise RuntimeError("No valid samples received; check the device, firmware and transport.")
        finally:
            print()

def demo(args, emit):
    # Measured timing uses firmware logic; only the input source is synthetic.
    from firmware.micropython.lab_core import LabCore
    lab = LabCore()
    start = time.monotonic()
    seq = 0
    while time.monotonic() - start < args.seconds:
        ms = int((time.monotonic() - start) * 1000)
        value = int((math.sin(ms / 1500) + 1) * 32767.5)
        lab.update(ms, value, False)
        if ms >= seq * 100:
            emit(Sample(seq & 65535, ms & 0xffffffff, value, int(lab.led),
                        0, 1, lab.period))
            seq += 1
        time.sleep(.005)

def serial_capture(args, emit):
    try:
        import serial
    except ImportError as exc:
        raise RuntimeError("Install host/requirements.txt to use serial") from exc
    deadline = time.monotonic() + args.seconds
    rejected = 0
    with serial.Serial(args.port, args.baud, timeout=1) as port:
        while time.monotonic() < deadline:
            line = port.read_until(b"\n", 256)
            if not line:
                continue
            if not line.endswith(b"\n"):
                rejected += 1
                continue
            try:
                emit(decode_line(line))
            except (ValueError, UnicodeError):
                rejected += 1
    print("\nRejected serial records:", rejected)

async def ble_capture(args, emit):
    try:
        from bleak import BleakClient
    except ImportError as exc:
        raise RuntimeError("Install host/requirements.txt to use BLE") from exc
    rejected = 0
    disconnected = asyncio.Event()
    def receive(_characteristic, data):
        nonlocal rejected
        try:
            emit(decode_packet(data))
        except ValueError:
            rejected += 1
    async with BleakClient(args.address,
                           disconnected_callback=lambda _: disconnected.set()) as client:
        await client.start_notify(DATA_UUID, receive)
        try:
            await asyncio.wait_for(disconnected.wait(), args.seconds)
        except asyncio.TimeoutError:
            pass
        else:
            raise RuntimeError("BLE disconnected; CSV retained. Scan and reconnect.")
        if client.is_connected:
            await client.stop_notify(DATA_UUID)
    print("\nRejected BLE records:", rejected)

async def scan():
    try:
        from bleak import BleakScanner
    except ImportError as exc:
        raise RuntimeError("Install host/requirements.txt to scan BLE") from exc
    devices = await BleakScanner.discover(timeout=5)
    for device in devices:
        print(device.address, device.name or "(unnamed)")
    print("Select your PathwaysLab identifier explicitly with ble --address.")

def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Must be a positive finite number")
    return number

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("scan", help="List BLE devices; does not connect")
    for command in ("demo", "serial", "ble"):
        sub = commands.add_parser(command)
        sub.add_argument("--seconds", type=positive, default=10)
        sub.add_argument("--csv", default="capture.csv")
        if command == "serial":
            sub.add_argument("--port", required=True)
            sub.add_argument("--baud", type=int, default=115200)
        if command == "ble":
            sub.add_argument("--address", required=True)
    args = parser.parse_args()
    try:
        if args.command == "scan":
            asyncio.run(scan())
        else:
            with output(args.csv) as emit:
                if args.command == "demo": demo(args, emit)
                elif args.command == "serial": serial_capture(args, emit)
                else: asyncio.run(ble_capture(args, emit))
    except KeyboardInterrupt:
        print("Capture stopped; CSV retained.")
    except (RuntimeError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")

if __name__ == "__main__":
    main()
