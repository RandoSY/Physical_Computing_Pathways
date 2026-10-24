# Programmer guide

## Separation of responsibilities

`LabCore` owns debounce, run/pause, LED state and period mapping. Board adapters
own pins, ADC reads, LED polarity and clock calls. Transport publishes a
snapshot every approximately 100 ms. The host validates records, displays a
gauge, writes CSV and creates an offline report.

The knob maps normalized input 0..65535 to a **full cycle** of 100..2000 ms:
`period_ms = 100 + input_u16 * 1900 // 65535`. Each LED half-cycle uses integer
`period_ms // 2`, so an odd requested period is rounded down by one millisecond
over a full cycle. Loop scheduling adds jitter. This is a teaching signal
generator, not a calibrated timing instrument.

A button must remain in its new state for 25 ms. Only the debounced press edge
toggles run. Pause forces the LED off. Resume starts a new half-cycle. A delayed
loop toggles once at the next opportunity; it does not replay missed edges.

C++ uses unsigned subtraction across the `millis()` wrap. MicroPython uses
`ticks_diff` and accumulates relative tick differences into a 32-bit wire clock.
The sampling loop must execute more often than half the MicroPython tick period.

## USB serial / CSV

Firmware sends one ASCII line, seven integer fields, at 115200 baud:

```text
seq,ms,input_u16,led,button,running,period_ms
0,100,32768,0,0,1,1050
```

The first line above is the **host CSV header**; firmware emits only data lines.
The serial decoder ignores startup/nonprotocol lines and counts rejected
records. Numeric bounds are validated. `input_u16` is normalized ADC counts,
not a claim of 16-bit ADC resolution or measured voltage.

| Field | Range | Meaning |
|---|---|---|
| seq | 0..65535 | Sample sequence, wraps modulo 65536 |
| ms | 0..4294967295 | Device-relative milliseconds, wraps modulo 2^32 |
| input_u16 | 0..65535 | Normalized input |
| led | 0 or 1 | Logical LED state, independent of polarity |
| button | 0 or 1 | Debounced pressed state for the full instrument |
| running | 0 or 1 | Run/pause state |
| period_ms | 100..2000 | Requested full blink period |

The simpler micro:bit bridge reports raw button state and its two fixed periods,
and always reports running=1. GCBASIC, STC and MSP430 black-box examples do not
emit this protocol.

## BLE service

- Service UUID: `56f90001-20bb-4c54-8b27-48a5e3351a4e`
- Data characteristic UUID: `56f90002-20bb-4c54-8b27-48a5e3351a4e`
- Characteristic permissions: read and notify; no write commands.
- Device name: `PathwaysLab`, customizable in board_config.py.
- Advertising data: flags and local name; service UUID in scan response.

Each notification is **12 bytes**, little-endian `struct` format `<BBHIHH`:

| Offset | Size | Value |
|---|---|---|
| 0 | 1 | Version = 1 |
| 1 | 1 | Flags: bit 0 LED, bit 1 button, bit 2 running; other bits zero |
| 2 | 2 | Sequence |
| 4 | 4 | Device milliseconds |
| 8 | 2 | Normalized input |
| 10 | 2 | Period milliseconds |

The fixed packet fits the default 20-byte ATT value payload; no fragmentation
or MTU negotiation is needed. Unknown versions, reserved flag bits, incorrect
lengths and out-of-range values are rejected. The most recent sample is also
readable. Before the first publish the characteristic may be empty.

Notifications are not a reliable archival transport. The host records sequence
discontinuities; those may mean dropped, repeated, reordered records or a reset.
The HTML trace plots sample index and does not imply continuous wall-clock time.
BLE disconnect ends host capture with an error and preserves the CSV. Restart
capture to reconnect. There is no automatic reconnect or bonded session.

## Porting

Start with an existing core and profile. Confirm GPIO numbers, ADC scale,
polarity, pull resistors, clock API and serial transport. Run host tests, compile
for the exact target, then execute the bench checklist. Add a profile only after
recording toolchain version and wiring; distinguish source availability from
tested compatibility in HARDWARE.md.

No secrets, cloud services or host credentials are required by the firmware.
