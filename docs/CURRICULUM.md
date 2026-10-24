# Instructor sequence

The organizing idea is a progression in programming experience:
**GCBASIC → Arduino IDE / C++ → MicroPython + BLE**.
The hardware families provide examples, rather than a claim that each language
works on every chip. Use branches to compare architectures without interrupting
the main learning route.

## 1. 8-Bit Classics: discover behavior

**A. PIC10 — The Black Box.** Present a programmed PIC10F322, an LED, and a
button before revealing the source. Ask students to predict and measure what
the button changes. Record the LED's on/off times. Reveal the GCBASIC source;
relate each instruction to an observable event. Change one wait interval and
predict the effect before programming.

**B. STC / 8051 branch.** Repeat the black-box challenge with the SDCC C source.
Explain why the compiler differs. Investigate I/O modes and how a software
delay depends on oscillator frequency and generated instructions. Do not use
this uncalibrated delay as a clock reference.

**C. ATmega328P — The Arduino Revolution.** Start with GCBASIC on the Uno, then
move to Arduino C++ on the **same board**. Holding the button changes timing in
the BASIC example; pressing once toggles run/pause in the C++ example. Have
students identify why these are different specifications. Add the pot and
compare blocking waits with a state machine that keeps sampling inputs.

Check: can the learner explain input, output, state, time and active-low logic
by pointing to real pins and measured observations?

## 2. ARM Mountain: make time and state explicit

**A. MSP430 base camp and the PDP-11 connection.** Use the MSP430G2553 example
and debugger to observe registers and a memory-mapped I/O port. Compare how
MSP430 and PDP-11 assembly express register operations, addressing, branches,
stack and subroutine concepts. This is an instructional comparison, not binary
compatibility or a claim of identical instruction sets. Then distinguish the
16-bit MSP430 from TI's Arm Cortex-M0+ MSPM0 family. An MSPM0 firmware port is
a later task after selecting an exact board.

**B. Pico RP2040.** Transfer the C++ instrument to profile 2. Keep the user
behavior identical; change only hardware mapping and toolchain. Inspect
`lab_core.h` separately from GPIO and Serial calls. Introduce an SWD debugger.
An extension can turn a second Pico into a debug probe; this repository does
not contain probe firmware. PIO and two-core designs are later exercises.

**C. STM32.** Choose a specific C0/G0 board/package, verify profile 3 pins,
and configure the corresponding Arduino core. Compare debugger observations
with physical timing. Explain why a portable state machine does not eliminate
board-specific initialization, electrical limits or serial routing.

Check: can the learner reproduce a button-bounce bug, explain its correction,
and distinguish host unit tests, target compilation and a bench experiment?

## 3. Wireless Wonders: turn measurements into instruments

**A. micro:bit V2.** Use the radio sender and receiver pair. Separate sensing,
transmission and host display. Record what happens when the sender is turned
off. Its button input is represented as 0/65535, not an analog reading.

**B. Pico W.** Port the familiar state machine to MicroPython. Explore values
at the REPL, then run `main.py`. Compare readable interpreted code with compiled
C++. Observe USB serial and BLE representations of the same measurements.

**C. ESP32 virtual instruments.** Use the C3 or S3 profile with external wiring.
Compare observed update interval, packet gaps and reconnection behavior.
Choose C6/H2 for a later protocol-specific project only after confirming the
firmware ecosystem and board variant. BLE, Wi-Fi and Zigbee are distinct
transports; this release implements BLE plus serial, not Zigbee or Wi-Fi.

Check: can the learner distinguish the device's sample time from host arrival
time, and identify aliasing when 10 Hz telemetry observes a faster signal?

## Common lab record

For every experiment record: exact board/chip marking; wiring diagram; supply;
compiler/firmware version; source commit; expected behavior; observed behavior;
capture filename; and explanation of differences. Keep measurements separate
from simulated data. Change one variable at a time.

Assessment is demonstration and explanation: predict → build → measure →
explain → improve. Finishing a sequence of boards is not by itself evidence
of understanding.
