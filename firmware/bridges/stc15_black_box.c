/* SDCC / STC15W408AS side branch. Not a GCBASIC target.
 * External active-low LED: VDD -> resistor -> LED -> P1.0.
 * P3.2 button to GND with external 10k pull-up.
 * Source-only: verify exact chip/package and oscillator before programming.
 * Delay is deliberately uncalibrated; measure it in the black-box experiment.
 */
__sfr __at (0x90) P1;
__sfr __at (0xB0) P3;
__sfr __at (0x91) P1M1;
__sfr __at (0x92) P1M0;
__sbit __at (0x90) LED;
__sbit __at (0xB2) BUTTON;

static void pause(unsigned char units) {
    volatile unsigned int i;
    while (units--) for (i = 0; i < 3000; ++i) {}
}

void main(void) {
    P1M1 &= ~1; P1M0 |= 1; /* P1.0 push-pull */
    BUTTON = 1; /* default quasi-bidirectional P3.2 input */
    LED = 1;
    while (1) {
        LED = 0; pause(BUTTON ? 5 : 1);
        LED = 1; pause(BUTTON ? 5 : 1);
    }
}
