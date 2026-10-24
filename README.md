# Physical Computing Pathways

**GCBASIC → Arduino IDE / C++ → MicroPython + BLE**

A hands-on curriculum initiated by Rando: **8-Bit Classics**, **ARM Mountain**,
and **Wireless Wonders & Virtual Instruments**. The progression is in the
programming experience as well as the hardware.

Make something happen. Organize and control its behavior. Connect it to other things.

## Start here — no board required

With Python 3.10 or later, open a terminal in this repository:

```sh
python -m host.instrument demo --seconds 10 --csv capture.csv
python -m host.report capture.csv --output trace.html
```

Open `trace.html` in a browser. This is **simulated data**, generated locally;
it does not claim that a physical board has been tested. No dependencies or
Internet connection are required for this demonstration.

## The shared experiment

The first BASIC lessons use a button to change LED timing. The C++ and
MicroPython instrument extends that behavior:

- Turn a potentiometer to set the full blink period from 100 to 2000 ms.
- Press a button to toggle run/pause; a 25 ms debounce prevents bounce toggles.
- Measure the output and compare expected and observed timing.
- Capture normalized input, LED state, button state, run state and period over USB or BLE.
- Review a CSV capture as an offline HTML instrument trace.

The instrument runs without a connected computer. Telemetry is observation;
it does not control the loop. Sampling is approximately 10 Hz. Short LED pulses
can be missed in telemetry; use a scope or logic analyzer for edge timing.

## Learning route

| Stage | Hardware | Software in this release |
|---|---|---|
| 8-Bit Classics | PIC10F322, ATmega328P | Two GCBASIC black-box lessons |
| 8-Bit side branch | STC15W408AS / 8051 | SDCC C black-box source; separate toolchain |
| ARM Mountain base camp | MSP430G2553; PDP-11 comparison | TI C example and architecture lesson |
| ARM Mountain | Pico RP2040, STM32 | Arduino C++ instrument with board profiles |
| Wireless Wonders | micro:bit V2 | MicroPython radio sender and USB receiver bridge |
| Wireless Wonders | Pico W, ESP32-C3/S3 | MicroPython BLE instrument source |
| Extension track | MSPM0, ESP32-C6/H2 | Planned ports; not delivered as working targets |

See [hardware and support](docs/HARDWARE.md) before flashing. Do not assume
that every language supports every board. In particular GCBASIC is not the
STC/8051 compiler, MSP430 is not Arm, and the supplied micro:bit radio lesson
does not use BLE.

## Guides

- [Quick start: Windows, Linux, macOS and device setup](docs/QUICKSTART.md)
- [Hardware, wiring and support matrix](docs/HARDWARE.md)
- [Instructor sequence and learning checks](docs/CURRICULUM.md)
- [Programmer guide and telemetry protocol](docs/PROTOCOL.md)
- [Validation record and next hardware checks](docs/VALIDATION.md)
- [Sources and toolchain references](docs/SOURCES.md)

## Repository layout

```text
firmware/gcbasic/             PIC and AVR BASIC lessons
firmware/arduino/PathwaysLab/  C++ instrument and board profiles
firmware/micropython/         Interactive instrument with BLE
firmware/bridges/             STC, MSP430 and micro:bit teaching branches
host/                        Demo, serial/BLE capture and HTML reporting
tests/                       Host protocol, state machine and BLE mock tests
docs/                        Instructor and programmer guides
```

## Development checks

```sh
python -m unittest discover -s tests -v
g++ -std=c++11 -Wall -Wextra -Werror tests/core_test.cpp -o core_test
```

Run the resulting `core_test` executable. GitHub Actions is configured to compile
the Uno sketch. A passing host test is not a hardware or radio validation.

**Release: 0.1.0 — initial teaching software.** No attached boards were available
during authoring. See the validation record for the exact checks performed.
Licensing has not been selected; no open-source license grant is implied.
