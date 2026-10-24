/* TI MSP430G2553 LaunchPad: red LED P1.0; S2 button P1.3.
 * Compile using a matching TI CCS MSP430G2553 project.
 * MSP430 is a 16-bit architecture, not an Arm core.
 */
#include <msp430.h>
int main(void) {
    WDTCTL = WDTPW | WDTHOLD;
    if (CALBC1_1MHZ == 0xFF) while (1) {} /* missing calibration */
    DCOCTL = 0;
    BCSCTL1 = CALBC1_1MHZ;
    DCOCTL = CALDCO_1MHZ;
    P1DIR |= BIT0;
    P1DIR &= ~BIT3;
    P1REN |= BIT3;
    P1OUT |= BIT3;
    P1OUT &= ~BIT0;
    while (1) {
        P1OUT ^= BIT0;
        if (P1IN & BIT3) __delay_cycles(500000);
        else __delay_cycles(100000);
    }
}
