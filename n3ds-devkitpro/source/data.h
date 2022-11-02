#pragma once
#include "info.h"

#define max_objects_pos 20

extern int current_screen;

// COLORS

extern u32 clrRed;

// Data Init function
void initData();

// GAME DATA

extern touchPosition touch;
extern u32 kDown;
extern u32 kHold;
extern u32 kUp;
