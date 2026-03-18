#ifndef BASIC_ROUTINES_H
#define BASIC_ROUTINES_H

#include "CONSTS.h"
#include <Keyboard.h>

void one_step(bool);

void set_steps(int16_t);
void set_angle(float);
void set_destination(float);
void print_steps();
void print_angle();
void print_destination();

bool in_destination();
void hard_move(float);

void homming();

void blink_Led(uint8_t, uint16_t, uint16_t);
void led_on();
void led_off();


#endif /* BASIC_ROUTINES_H */
