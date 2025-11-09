from pico2d import *
import play_modes.Town_mode
import screen.mainScreen
import game_framework
screen.mainScreen.init()


#game_framework.run(screen.mainScreen)
SDL_SetRenderDrawBlendMode(pico2d.renderer, SDL_BLENDMODE_BLEND)
game_framework.run(play_modes.Town_mode)



close_canvas()