#pragma once
// 1 = Uno R3 + common multifunction shield; 2 = original Pico RP2040;
// 3 = STM32 custom wiring example (select matching MCU/variant in Arduino IDE).
#ifndef PATHWAYS_BOARD
#define PATHWAYS_BOARD 1
#endif
#if PATHWAYS_BOARD == 1
constexpr int LED_PIN = 13, BUTTON_PIN = A1, INPUT_PIN = A0;
constexpr bool LED_ACTIVE_LOW = true;
constexpr uint32_t ADC_MAX = 1023;
#elif PATHWAYS_BOARD == 2
constexpr int LED_PIN = 15, BUTTON_PIN = 14, INPUT_PIN = 26;
constexpr bool LED_ACTIVE_LOW = false;
constexpr uint32_t ADC_MAX = 1023; // explicitly request 10-bit ADC in setup
#elif PATHWAYS_BOARD == 3
constexpr int LED_PIN = PB0, BUTTON_PIN = PB1, INPUT_PIN = PA0;
constexpr bool LED_ACTIVE_LOW = false;
constexpr uint32_t ADC_MAX = 1023;
#else
#error Unsupported PATHWAYS_BOARD; choose 1, 2, or 3
#endif
