# Pick one profile before uploading. External LEDs avoid clone LED differences.
BOARD = "pico_w"  # pico_w, esp32_c3, esp32_s3
NAME = "PathwaysLab"
PROFILES = {
    "pico_w": {"led": 15, "button": 14, "adc": 26},
    "esp32_c3": {"led": 3, "button": 4, "adc": 0},
    "esp32_s3": {"led": 5, "button": 4, "adc": 1},
}
