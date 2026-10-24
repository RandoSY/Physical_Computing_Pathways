# Flash onto the USB-connected micro:bit. Capture its serial port at 115200.
from microbit import sleep, uart
import radio
uart.init(baudrate=115200)
radio.config(group=42, channel=7, length=64)
radio.on()
while True:
    message = radio.receive()
    if message is not None:
        uart.write(message + "\n")
    sleep(5)
