# Quick start

## Host tools

Install Python 3.10+ and Git. Clone the project after it is published, or extract
the project archive. Open a terminal in the directory containing README.md.
On Windows, `py` may be used wherever this guide says `python`.

First try the dependency-free demo:

```sh
python -m host.instrument demo --seconds 10 --csv capture.csv
python -m host.report capture.csv --output trace.html
```

Open `trace.html`. The console has a live input gauge; the report contains a
recorded trace and last 25 records. Demo input is synthetic.

For USB or BLE, create a virtual environment:

```sh
python -m venv .venv
```

Windows PowerShell (activation is optional):

```powershell
.\.venv\Scripts\python.exe -m pip install -r host/requirements.txt
.\.venv\Scripts\python.exe -m host.instrument scan
```

Linux/macOS:

```sh
.venv/bin/python -m pip install -r host/requirements.txt
.venv/bin/python -m host.instrument scan
```

Use that same environment's Python for subsequent commands. BLE requires an
enabled BLE adapter and OS Bluetooth permissions. Serial requires a suitable
USB data cable, device driver and port access. Close any IDE serial monitor
before running the capture tool. No Docker or server is required.

## Arduino IDE / C++

1. Open `firmware/arduino/PathwaysLab/PathwaysLab.ino` in Arduino IDE.
2. Start with Uno R3 and the common multifunction shield. Install the Arduino
   AVR Boards package, select Arduino Uno, then the actual serial port.
3. Verify the shield wiring against HARDWARE.md; compile and upload.
4. Turn the pot. Press S1 once to pause and again to resume.
5. Close Serial Monitor and capture (replace COM5 with the actual port):

```sh
python -m host.instrument serial --port COM5 --seconds 30 --csv capture.csv
python -m host.report capture.csv --output trace.html
```

Linux ports may look like `/dev/ttyACM0`; macOS ports like `/dev/cu.usbmodem...`.
Do not copy an example port without checking it.

For Pico, install the Arduino-Pico core linked in SOURCES.md and change
`PATHWAYS_BOARD` to 2 in `board_config.h`. Select the original Raspberry Pi
Pico board and wire the external circuit. For STM32 use profile 3, install
STM32duino, select the exact chip/package and serial configuration, and adjust
pins to the actual board. These two targets still need compiler and bench
verification; the Uno profile is the initial validation target.

Command-line Uno build:

```sh
arduino-cli core update-index
arduino-cli core install arduino:avr@1.8.6
arduino-cli compile --fqbn arduino:avr:uno --warnings all firmware/arduino/PathwaysLab
```

## GCBASIC

Install GCBASIC from its official distribution. Open the relevant `.gcb` file
in its IDE, compile for the `#chip` target, inspect code size and warnings, then
program using the appropriate tool. PIC10F322 needs a compatible PIC ICSP
programmer; an Uno may use its serial bootloader with the correct uploader.
Compiler, configuration bits and programmer support must match the exact chip.
Do not alter AVR fuses or PIC configuration values by copying settings from a
different device. No precompiled binaries are distributed in this release.

Measure the blink period with and without the button held. The BASIC programs
use blocking waits on purpose; the next C++ lesson removes that limitation.

## MicroPython + BLE

1. Install official MicroPython firmware for the **exact** Pico W, ESP32-C3
   or ESP32-S3 board/flash configuration using its download page instructions.
   Plain Pico RP2040 has no onboard radio; Pico W is required for this lesson.
2. At the REPL, check `import bluetooth` and `bluetooth.BLE()`.
3. Edit `BOARD` in `firmware/micropython/board_config.py`.
4. Copy all four `.py` files in that directory onto the board filesystem using
   Thonny or `mpremote`. Keep `main.py`, `board_config.py`, `lab_core.py` and
   `ble_instrument.py` together.
5. Reset. The device advertises as `PathwaysLab`, runs the LED experiment and
   prints serial telemetry. Ctrl-C at the REPL stops it; rename `main.py` if
   you need to prevent automatic start during troubleshooting.
6. Find its BLE identifier, then connect explicitly:

```sh
python -m host.instrument scan
python -m host.instrument ble --address YOUR_DEVICE_IDENTIFIER --seconds 30 --csv capture.csv
python -m host.report capture.csv --output trace.html
```

On macOS the identifier can be a UUID rather than a MAC address. With several
devices, give each a distinct `NAME`, scan, and select the intended device.
Capture stops on disconnect and retains its CSV; repeat scan and capture to
reconnect. Firmware resumes advertising after a peer disconnects.

BLE telemetry is readable without pairing; this is an educational instrument
for non-sensitive bench signals. There is no BLE command or remote-actuator
write characteristic.

## Other branches

- STC: verify the part is STC15W408AS; compile with SDCC's mcs51 target and
  use a chip-compatible STC ISP procedure. `sdcc -mmcs51 firmware/bridges/stc15_black_box.c`
  produces an Intel hex-format `.ihx` image. Clock/delay calibration is a lab task.
- MSP430: create a TI CCS MSP430G2553 C project, replace its main source with
  `msp430g2553_black_box.c`, and program the LaunchPad. Do not select MSPM0.
- micro:bit: flash the sender to one V2 and the receiver to another using the
  micro:bit Python editor. Plug the receiver into the host and use the serial
  capture command. Group/channel are classroom settings, not security controls.
