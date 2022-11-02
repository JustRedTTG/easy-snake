#pragma once

#include <citro2d.h>

#include <string.h>
#include <stdio.h>
#include <stdlib.h>


#define SCREEN_WIDTH  400
#define SCREEN_WIDTH_BOT  320
#define SCREEN_HEIGHT 240
#define CONFIG_3D_SLIDERSTATE (*(volatile float*)0x1FF81080)

void draw();

extern bool depth_mode;
extern bool debug;
extern int debug_level;
extern u32 clrClear;
extern u32 botclrClear;
