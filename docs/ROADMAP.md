# Project roadmap

## 0.1 — software foundation

- GCBASIC PIC10 and AVR black-box sources.
- Arduino serial instrument with isolated state machine and three pin profiles.
- MicroPython BLE instrument with Pico W and C3/S3 wiring profiles.
- STC/8051, MSP430 and micro:bit radio teaching branches.
- Host simulator, USB/BLE capture, CSV, recorded HTML trace and automated tests.
- Instructor sequence and explicit target-support status.

## 0.2 — validate the bench

1. Compile and flash GCBASIC PIC10F322 and Uno programs; record code sizes.
2. Check the exact multifunction shield revision; demonstrate Uno input,
   debounce, output timing and serial capture.
3. Validate Pico W BLE to Windows 11, including disconnect and reconnect.
4. Confirm STC chip marking; compile with SDCC and characterize its delay.
5. Validate MSP430G2553, Pico and the selected STM32 target with a debugger.
6. Validate C3/S3 pin mappings and ADC endpoints; capture firmware/tool versions.
7. Demonstrate two micro:bits and measure packet loss under classroom conditions.

## 0.3 — richer instruments

- Multifunction shield numeric display and tone-generation lessons.
- Timestamped edge captures to measure timing more precisely than 10 Hz telemetry.
- Interactive plotting and calibrated measurements with explicit uncertainty.
- PIO experiments and a documented second-Pico debugger workflow.
- MSPM0 port after an exact target is selected.
- C6/H2 ports with an explicit choice of BLE or 802.15.4 toolchain.

Keep this curriculum independent of unrelated monitoring or fitness systems.
Portable development and reproducible Git history are the project handoff.
