#include "data.h"

int current_screen = 0;

// COLORS
u32 clrRed;
u32 clrBlack;
u32 clrWhite;

void initData() {
    // COLOR NAME           =       C2D_Color32(0xRR, 0xGG, 0xBB, 0xAA);// (RRR, GGG, BBB)
    clrRed =                        C2D_Color32(0xFF, 0x00, 0x00, 0xFF);// (255, 0,   0  )
    clrBlack =                      C2D_Color32(0x00, 0x00, 0x00, 0xFF);// (0  , 0,   0  )
    clrWhite =                      C2D_Color32(0xFF, 0xFF, 0xFF, 0xFF);// (255, 255, 255)
}

// GAME DATA

touchPosition touch;
u32 kDown;
u32 kHold;
u32 kUp;

int offset_x = 80;
int offset_y = 0;

int board_size = 25;
int time_in_milliseconds_till_movement = 120;

int snake_size;
int snake_direction;
int snake_begin_size = 3;

void initializer_board() {
    snake_size = snake_begin_size;
}
