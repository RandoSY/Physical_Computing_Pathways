# micro:bit V2 MicroPython teaching bridge; proprietary radio, NOT BLE.
# A+B selection is unnecessary: flash receiver code on a second micro:bit.
from microbit import button_a, display, running_time, sleep, Image
import radio
radio.config(group=42, channel=7, length=64)
radio.on()
seq = 0
led = False
edge = 0
while True:
    ms = running_time()
    button = int(button_a.is_pressed())
    period = 200 if button else 1000
    if ms - edge >= period // 2:
        edge = ms
        led = not led
        if led: display.show(Image.HEART)
        else: display.clear()
    # Protocol-compatible normalized input is binary button state in this lesson.
    radio.send("{},{},{},{},{},1,{}".format(seq, ms & 0xffffffff,
               button * 65535, int(led), button, period))
    seq = (seq + 1) & 65535
    sleep(100)
