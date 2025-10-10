from pico2d import *
from screen.background import Background
from player.character import Character
from player.character import Bubble
from handeEvent import handle_events
from Town import Town
from current_map import CurrentMap
from screen.mainScreen import main_screen
width, height =  1400, 800
frame_character=0
open_canvas(width, height)



world=[]
background = Background()
current_Map = CurrentMap()

player = Character(200, 300)
def world_reset():
    global current_Map
    if (current_Map.current_map == 0):
        world.clear()
        # 메인 스크란 추가
        world.append(background)
        main_screen1 = main_screen()
        world.append(main_screen1)
    if (current_Map.current_map == 1):
        world.clear()

        global player
        current_Map.change_map(1)

        town = Town()
        world.append(town)

        player = Character(200, 300)
        world.append(player)

def world_update():
    global current_Map
    if (current_Map.current_map == 0):
        handle_events(player,world,current_Map)
        if current_Map.current_map == 1:
            world_reset()

    if (current_Map.current_map == 1):
        handle_events(player,world,current_Map)

        player.update_frame(0.05)
        for obj in world:
            if isinstance(obj, Bubble):
                obj.update()
        player.move(current_Map)

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