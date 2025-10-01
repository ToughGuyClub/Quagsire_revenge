from pico2d import *
from background import Background
from character import Character
from handeEvent import handle_events
from Town import Town

width, height =  1400, 800
frame_character=0
open_canvas(width, height)



world=[]

def world_reset():
    world.clear()

    global player

    backgrounds = Background()
    world.append(backgrounds)

    town = Town()
    world.append(town)



    player = Character(200, 200)
    world.append(player)

def world_update():
    handle_events(player)
    player.update_frame(0.05)
    player.move()



def wolrd_draw():

    for obj in world:
        obj.draw()



world_reset()
while True:
    clear_canvas()


    world_update()
    wolrd_draw()



    update_canvas()
    delay(0.02)


close_canvas()