from machine import Pin, ADC
import time
from board_config import BOARD, NAME, PROFILES
from lab_core import LabCore
from ble_instrument import Instrument

pins = PROFILES[BOARD]
led = Pin(pins["led"], Pin.OUT, value=0)
button = Pin(pins["button"], Pin.IN, Pin.PULL_UP)
adc = ADC(Pin(pins["adc"]))
if BOARD.startswith("esp32"):
    adc.atten(ADC.ATTN_11DB)
instrument = Instrument(NAME)
lab = LabCore(time.ticks_diff)
previous = time.ticks_ms()
lab.edge = lab.changed = previous
last_report = previous
elapsed = 0
sequence = 0
try:
    while True:
        now = time.ticks_ms()
        elapsed = (elapsed + time.ticks_diff(now, previous)) & 0xffffffff
        previous = now
        lab.update(now, adc.read_u16(), not button.value())
        led.value(lab.led)
        if time.ticks_diff(now, last_report) >= 100:
            last_report = now
            instrument.publish(sequence, elapsed, lab)
            print("{},{},{},{},{},{},{}".format(sequence, elapsed, lab.input,
                  int(lab.led), int(lab.button), int(lab.running), lab.period))
            sequence = (sequence + 1) & 65535
        time.sleep_ms(5)
finally:
    led.off()
    instrument.ble.active(False)
