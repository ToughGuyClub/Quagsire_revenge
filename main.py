from pico2d import *
import play_modes.play_mode
import screen.mainScreen

screen.mainScreen.init()
while True:
    clear_canvas()

    screen.mainScreen.update()
    screen.mainScreen.draw()



    update_canvas()
    delay(0.012)


close_canvas()