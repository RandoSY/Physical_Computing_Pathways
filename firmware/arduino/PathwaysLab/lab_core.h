#pragma once
#include <stdint.h>

// Hardware-independent, rollover-safe state machine. One press toggles RUN.
class LabCore {
 public:
  bool led = false, running = true, button = false;
  uint16_t input = 0, period = 100;
  void update(uint32_t now, uint16_t value, bool pressed) {
    input = value;
    period = 100u + (uint32_t(value) * 1900u / 65535u);
    if (pressed != candidate) { candidate = pressed; changed = now; }
    if (candidate != button && uint32_t(now - changed) >= 25u) {
      button = candidate;
      if (button) { running = !running; led = false; edge = now; }
    }
    if (!running) { led = false; return; }
    if (uint32_t(now - edge) >= period / 2u) { led = !led; edge = now; }
  }
 private:
  bool candidate = false;
  uint32_t changed = 0, edge = 0;
};
