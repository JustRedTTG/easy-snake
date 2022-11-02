#include "info.h"
#include "data.h"

bool depth_mode = false;
bool debug = true;
int debug_level = 0;
// -1 - enables debug screen
// -2 - enables 3D debug values

int main(int argc, char* argv[]) {
    // INIT
	gfxInitDefault();
	C3D_Init(C3D_DEFAULT_CMDBUF_SIZE);
	C2D_Init(C2D_DEFAULT_MAX_OBJECTS);
	C2D_Prepare();
	gfxSet3D(false);

	// Display buffers
	C3D_RenderTarget* top = C2D_CreateScreenTarget(GFX_TOP, GFX_LEFT);
	C3D_RenderTarget* top_r = C2D_CreateScreenTarget(GFX_TOP, GFX_RIGHT);
	C3D_RenderTarget* bot = C2D_CreateScreenTarget(GFX_BOTTOM, GFX_LEFT);
	if (debug && debug_level < 0) {consoleInit(GFX_BOTTOM, NULL);}
	initData();
	u32 clrClear = C2D_Color32(0x00, 0x00, 0x00, 0xFF);
	u32 botclrClear = C2D_Color32(0x00, 0x00, 0x00, 0xFF);

	// Main loop
	while (aptMainLoop())
	{
	    depth_mode = false;
		hidScanInput();
		hidTouchRead(&touch);

		// Respond to user input
        kDown = hidKeysDown();
        kUp = hidKeysUp();
		kHold = hidKeysHeld();
		if (kDown & KEY_START) {/*save();*/break;}
		// DRAW
		C3D_FrameBegin(C3D_FRAME_SYNCDRAW);
		C2D_TargetClear(top, clrClear);
        C2D_SceneBegin(top);

        draw(-1);

        //if (CONFIG_3D_SLIDERSTATE > 0.0f){
        //    C2D_TargetClear(top_r, clrClear);
        //    C2D_SceneBegin(top_r);
        //    depth_mode = true;
        //    draw(1);
        //}
        if (debug_level > -1){
            C2D_TargetClear(bot, botclrClear);
            C2D_SceneBegin(bot);

            draw_bottom();
        }
		C3D_FrameEnd(0);
	}
	C2D_Fini();
	C3D_Fini();
	gfxExit();
	return 0;
}
