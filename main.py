import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import time

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

min_noise = 24000
max_noise = 38000

led_pins = [
    board.IO21,
    board.IO26, # type: ignore
    board.IO47,
    board.IO33,
    board.IO34,
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39
]

leds = [DigitalInOut(pin) for pin in led_pins]

for led in leds:
    led.direction = Direction.OUTPUT

update_interval = 0.01

last_update_time = time.monotonic()

old_target_index = 0

while True:
    volume = microphone.value


    noise_range = max_noise - min_noise

    normal = (volume-min_noise)/ noise_range

    normal = max(normal, 0)
    normal = min(normal, 1)

    target_index = int((len(led_pins)) * normal)

    current_time = time.monotonic()
    if (current_time - last_update_time >= update_interval):
        for i in range(len(led_pins)):
            leds[i].value = 0
        for i in range(target_index):
            leds[i].value = 1
        last_update_time = current_time

    old_target_index = target_index
    time.sleep(0.01)
