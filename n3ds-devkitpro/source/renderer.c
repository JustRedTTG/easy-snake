#include "draw.h"


void draw(int mult) {
    if (current_screen == 0){
        draw_rect_center(SCREEN_WIDTH * .5, SCREEN_HEIGHT * .5,
                         SCREEN_WIDTH * .2, SCREEN_WIDTH * .2,
                         clrRed, 5 * mult * CONFIG_3D_SLIDERSTATE, 0);
    }
}

void draw_bottom() {
    if (current_screen == 0){
        draw_rect_center(SCREEN_WIDTH_BOT * .5, SCREEN_HEIGHT * .5,
                         SCREEN_WIDTH_BOT * .2, SCREEN_WIDTH_BOT * .2,
                         clrRed, 0, 0);
    }
}
