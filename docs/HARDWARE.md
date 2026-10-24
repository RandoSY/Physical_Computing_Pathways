# Hardware and support

## What is included

| Target | Toolchain | Implementation | Status before bench testing |
|---|---|---|---|
| PIC10F322 | GCBASIC + appropriate PIC programmer | Button-controlled blink | Source only; target compiler not run |
| ATmega328P / Uno R3 | GCBASIC | Button-controlled blink | Source only; target compiler not run |
| Uno R3 + common multifunction shield | Arduino AVR | Full serial instrument | See VALIDATION.md for compiler result |
| Original Pico / RP2040 | Arduino-Pico core | Full serial instrument, profile 2 | Source provided; target compiler not run |
| STM32 | STM32duino core | Full serial instrument, profile 3 | Custom wiring example; exact MCU/variant required |
| STC15W408AS | SDCC mcs51 | Button-controlled blink | Source only; exact part number still to confirm |
| MSP430G2553 LaunchPad | TI CCS MSP430 compiler | Button-controlled blink | Source only; target compiler not run |
| micro:bit V2 | micro:bit MicroPython | Radio sender/receiver | Source only; radio not bench tested |
| Pico W | Standard MicroPython build with bluetooth | Full BLE/serial instrument | Python syntax and mocks checked; hardware not tested |
| ESP32-C3/S3 | Matching MicroPython build with bluetooth | Full BLE/serial instrument | Python syntax and mocks checked; hardware not tested |
| MSPM0 | TI toolchain | Architecture transition only | Planned firmware port |
| ESP32-C6/H2 | Board-specific choice pending | Roadmap only | No firmware support claimed |

The original outline said STC18W408AS. STC's published family includes
STC15W408AS; verify the actual chip marking before using the STC example.

## Wiring for the full instrument

Use a 10k linear potentiometer, a normally open button, and an LED with a 1k
series resistor. Connect the potentiometer ends to the board's logic supply
and ground, its wiper to the ADC pin. Connect the button to ground; firmware
enables the internal pull-up. External LEDs are active-high: GPIO → resistor
→ LED anode; cathode → ground. All grounds must be common.

**Pico, STM32 and ESP32 examples use 3.3 V circuitry. Do not feed them the Uno
shield's 5 V signals.** GPIO numbers below are signal names, not physical
package pin numbers. Consult the particular board's pinout.

| Profile | ADC wiper | Button | LED | Supply |
|---|---|---|---|---|
| Uno + common multifunction shield | A0, onboard pot | A1, S1 | D13, active-low | Shield provides wiring |
| Arduino Pico, profile 2 | GP26 | GP14 | GP15 external | 3.3 V |
| Arduino STM32, profile 3 | PA0 | PB1 | PB0 external | 3.3 V |
| MicroPython `pico_w` | GP26 | GP14 | GP15 external | 3.3 V |
| MicroPython `esp32_c3` | GPIO0 | GPIO4 | GPIO3 external | 3.3 V |
| MicroPython `esp32_s3` | GPIO1 | GPIO4 | GPIO5 external | 3.3 V |

The STM32 pins are an example, not a promise that every C0/G0 package exposes
them. Check package pins, USB/serial availability and debugger routing first.
The C3 example deliberately uses an external LED instead of assuming the
onboard Super Mini LED's polarity. ESP32 ADC counts are not calibrated volts;
ADC attenuation, range, nonlinearities and saturation vary by chip.

## PIC10 black box

Breadboard wiring: RA0 drives an LED through 1k to ground; RA2 connects to a
button to ground with an external 10k pull-up to VDD. Add a 100 nF bypass
capacitor across VDD/GND, connect all required power pins and use the exact
PIC10F322 package diagram. Preserve ICSP clock/data/reset access.

The uploaded AC103011 is a PIC10F32X development board. This source intentionally
uses external breadboard wiring. Do not assume that the AC103011 LED or knob
matches these pins; adapt from its schematic before programming it.

## Multifunction shield

The default C++ profile assumes the widespread Uno shield with LEDs D10–D13,
buttons A1–A3, potentiometer A0, active-low buzzer D3, and 74HC595 display
latch D4 / clock D7 / data D8. Verify the clone schematic. This first release
uses D13, S1 and the pot; it silences the buzzer and blanks the display.
Numeric display and tone lessons are extension exercises, not finished drivers.

## micro:bit and BLE

The provided micro:bit source uses the MicroPython `radio` API between two
micro:bits; the receiver forwards text via USB serial. It is not Bluetooth.
For the BLE stage, use the supplied Pico W or C3/S3 instrument and a MicroPython
build that exposes `bluetooth.BLE`. A C6/H2 hardware BLE capability alone does
not establish compatibility with the provided MicroPython program. H2 has no
Wi-Fi; choose its future firmware for BLE/802.15.4 work specifically.
