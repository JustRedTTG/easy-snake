#include "data.h"

int current_screen = 0;

// COLORS
u32 clrRed;

void initData() {
    // COLOR NAME           =       C2D_Color32(0xRR, 0xGG, 0xBB, 0xAA);// (RRR, GGG, BBB)
    clrRed =                        C2D_Color32(0xFF, 0x00, 0x00, 0xFF);// (255, 0,   0  )
}

// GAME DATA

touchPosition touch;
u32 kDown;
u32 kHold;
u32 kUp;
