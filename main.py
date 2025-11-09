from pico2d import *
import play_modes.Town_mode
import screen.mainScreen
import game_framework
screen.mainScreen.init()


#game_framework.run(screen.mainScreen)
game_framework.run(play_modes.Town_mode)



close_canvas()