#include <Arduino.h>
#include "board_config.h"
#include "lab_core.h"

LabCore lab;
uint32_t lastReport = 0;
uint16_t sequence = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LED_ACTIVE_LOW ? HIGH : LOW);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
#if PATHWAYS_BOARD == 1
  // Common shield: keep buzzer and unused active-low LEDs off.
  for (int pin = 10; pin <= 12; ++pin) {
    pinMode(pin, OUTPUT); digitalWrite(pin, HIGH);
  }
  pinMode(3, OUTPUT); digitalWrite(3, HIGH);
  // Blank the usual 74HC595 display; verify clone wiring before use.
  pinMode(4, OUTPUT); pinMode(7, OUTPUT); pinMode(8, OUTPUT);
  digitalWrite(4, LOW);
  shiftOut(8, 7, MSBFIRST, 0xFF); shiftOut(8, 7, MSBFIRST, 0x00);
  digitalWrite(4, HIGH);
#else
  analogReadResolution(10);
#endif
  Serial.begin(115200);
  // No while(!Serial): firmware runs autonomously with no host attached.
}

void loop() {
  const uint32_t now = millis();
  const uint16_t value = uint32_t(analogRead(INPUT_PIN)) * 65535UL / ADC_MAX;
  lab.update(now, value, digitalRead(BUTTON_PIN) == LOW);
  digitalWrite(LED_PIN, (lab.led != LED_ACTIVE_LOW) ? HIGH : LOW);
  if (uint32_t(now - lastReport) >= 100u) {
    lastReport = now;
    Serial.print(sequence++); Serial.print(',');
    Serial.print(now); Serial.print(',');
    Serial.print(lab.input); Serial.print(',');
    Serial.print(lab.led); Serial.print(',');
    Serial.print(lab.button); Serial.print(',');
    Serial.print(lab.running); Serial.print(',');
    Serial.println(lab.period);
  }
}
