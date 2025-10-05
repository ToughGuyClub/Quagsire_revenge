from pico2d import *
from background import Background
from character import Character
from character import Bubble
from handeEvent import handle_events
from Town import Town
from current_map import CurrentMap

width, height =  1400, 800
frame_character=0
open_canvas(width, height)



world=[]
backgrounds= Background()
current_Map = CurrentMap()
def world_reset():
    world.clear()

    global player
    global current_Map
    current_Map.change_map(1)



    town = Town()
    world.append(town)



    player = Character(200, 300)
    world.append(player)

def world_update():
    handle_events(player,world)
    player.update_frame(0.05)
    for obj in world:
        if isinstance(obj, Bubble):
            obj.update()
    player.move(current_Map)

def wolrd_draw():
    global backgrounds
    backgrounds.draw()
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