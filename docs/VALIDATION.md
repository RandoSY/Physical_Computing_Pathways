# Validation record — 2026-10-24

Release candidate 0.1.0. No physical microcontroller was attached to this
authoring environment. No firmware was flashed and no live BLE transmission
was measured.

## Passed locally

| Check | Result |
|---|---|
| Python 3.12.14 syntax compilation | All host, firmware Python and test modules parse |
| Python unit tests | 13 passed |
| Native C++ core checks | Passed with g++ 13, C++11, -Wall -Wextra -Werror |
| Simulated host capture | Valid CSV generated without third-party packages |
| Offline HTML report | Generated from simulated capture |
| Arduino Uno target compilation | Passed; Arduino CLI 1.3.1, AVR core 1.8.6 |
| Uno flash usage | 2,962 / 32,256 bytes (9%) |
| Uno static RAM usage | 210 / 2,048 bytes (10%) |

The Arduino core emitted unused-parameter warnings in its own `new.cpp`.
No sketch warning was emitted. Initial package download through Arduino CLI
failed because its network path was unavailable. Official Arduino archives
were then downloaded into the package cache, verified against registry
checksums, installed and compiled successfully.

The Python checks cover packet and text decoding, invalid inputs, sequence
wrap in reports, empty captures, period endpoints, LED timing, debounce,
held-button behavior, pause/resume, tick rollover, BLE packet generation and
disconnect/re-advertise behavior using a mock radio. The C++ executable checks
timing, debounce, pause/resume and unsigned timer rollover.

GitHub Actions is configured for host/core tests and Uno compilation. It has
not been run remotely as part of this record. No claim is made that host
mocks validate a specific MicroPython firmware build or physical radio.

## Not yet validated

- GCBASIC PIC10F322/ATmega328P target compilation and programming.
- SDCC/STC and TI/MSP430 target compilation.
- Pico and STM32 Arduino target compilation and pin configuration.
- MicroPython installation, pin wiring and BLE on Pico W or ESP32-C3/S3.
- micro:bit sender/receiver radio and serial behavior.
- Timing accuracy, ADC range, electrical behavior, actual disconnect recovery.
- MSPM0 and C6/H2 ports, which remain roadmap items.

## First bench acceptance

1. Record board model, chip marking, supply, wiring and firmware/tool versions.
2. Start with Uno R3, confirm the multifunction shield pinout, and upload.
3. Check LED starts and the pot changes the requested period 100..2000 ms.
4. Press S1: LED pauses off. Hold it: no repeated toggles. Release and press:
   LED resumes. Test bounce and rapid pressing.
5. Capture 30 seconds of serial output. Confirm all seven fields and sequence.
6. Remove the host connection while supplying suitable board power: firmware
   must continue operating. Verify electrical conditions before changing power.
7. Repeat on Pico W after firmware installation. Scan, connect, receive
   notifications, disconnect, scan and reconnect. Record actual results.
8. Use a scope/logic analyzer for edge timing; do not infer sub-100 ms behavior
   from the 10 Hz telemetry stream.

Promote a target from source-only to bench-validated only after recording these
observations, the source commit and the exact toolchain.
