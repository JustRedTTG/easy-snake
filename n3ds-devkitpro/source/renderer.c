#include "draw.h"


void draw(int mult) {
    draw_rect_center(SCREEN_WIDTH * .5, SCREEN_HEIGHT * .5, SCREEN_HEIGHT, SCREEN_HEIGHT,
                     clrBlack, 0, 0);
    draw_rect_center(SCREEN_WIDTH * .5, SCREEN_HEIGHT * .5, SCREEN_HEIGHT, SCREEN_HEIGHT,
                     clrWhite, 0, 2);
}

void draw_bottom() {
}
