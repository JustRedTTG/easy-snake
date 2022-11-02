#pragma once
#include "info.h"

#define max_objects_pos 20

extern int current_screen;

// COLORS

extern u32 clrRed;
extern u32 clrBlack;
extern u32 clrWhite;

// Data Init function
void initData();

// GAME DATA

extern touchPosition touch;
extern u32 kDown;
extern u32 kHold;
extern u32 kUp;

extern int offset_x;
extern int offset_y;

extern int board_size;
extern int time_in_milliseconds_till_movement;

extern int snake_size;
extern int snake_direction;
extern int snake_begin_size;
