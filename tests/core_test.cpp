#include <cassert>
#include <iostream>
#include "../firmware/arduino/PathwaysLab/lab_core.h"
int main() {
  LabCore lab;
  lab.update(0, 65535, false); assert(lab.period == 2000);
  lab.update(0, 0, false); assert(lab.period == 100);
  lab.update(49, 0, false); assert(!lab.led);
  lab.update(50, 0, false); assert(lab.led);
  lab.update(51, 0, true); lab.update(75, 0, true); assert(lab.running);
  lab.update(76, 0, true); assert(!lab.running && !lab.led);
  lab.update(10000, 0, true); assert(!lab.running);
  lab.update(10001, 0, false); lab.update(10026, 0, false);
  lab.update(10027, 0, true); lab.update(10052, 0, true); assert(lab.running);
  LabCore bounce;
  bounce.update(1, 0, true); bounce.update(5, 0, false);
  bounce.update(100, 0, false); assert(bounce.running);
  LabCore wrap;
  wrap.update(0xfffffff0u, 0, false); assert(wrap.led);
  wrap.update(34u, 0, false); assert(!wrap.led);
  wrap.update(0xfffffff0u, 0, true); wrap.update(9u, 0, true);
  assert(!wrap.running);
  std::cout << "C++ core: timing, debounce, pause/resume, rollover passed\n";
}
