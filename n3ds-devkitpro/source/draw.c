#include "draw.h"

void draw_rect_center(int x, int y, int w, int h, u32 clr, double depth_math, int width) {
    if (width < 0) {return;}
    if (width == 0) {C2D_DrawRectSolid(x - w * .5 + depth_math, y - h * .5,0,w,h,clr);return;}

    int rectX = x - w * .5 + depth_math;
    int rectY = y - h * .5;
    C2D_DrawLine(rectX,rectY,clr, rectX+w,rectY,clr,width,0);
    C2D_DrawLine(rectX,rectY + h,clr, rectX+w,rectY + h,clr,width,0);
    C2D_DrawLine(rectX,rectY,clr, rectX,rectY+h,clr,width,0);
    C2D_DrawLine(rectX+w,rectY,clr, rectX+w,rectY+h,clr,width,0);
}

void draw_rect(int x, int y, int w, int h, u32 clr, double depth_math, int width) {
    if (width < 0) {return;}
    if (width == 0) {C2D_DrawRectSolid(x + depth_math, y,0,w,h,clr);return;}

    int rectX = x + depth_math;
    int rectY = y;
    C2D_DrawLine(rectX,rectY,clr, rectX+w,rectY,clr,width,0); // Top
    C2D_DrawLine(rectX,rectY + h,clr, rectX+w,rectY + h,clr,width,0); // Bottom
    C2D_DrawLine(rectX,rectY,clr, rectX,rectY+h,clr,width,0); // Left
    C2D_DrawLine(rectX+w,rectY,clr, rectX+w,rectY+h,clr,width,0); // Right
}
