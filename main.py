from pico2d import *
from screen.background import Background
from player.character import Character
from player.character import Bubble
from handeEvent import handle_events
from map.town.Town import Town
from current_map import CurrentMap
from screen.mainScreen import main_screen
from screen.intro import intro_screen
from enemy.Enemy import Enemy
from player.player_UI import Player_UI
from collision_check import collision_player_object
width, height =  1400, 800
frame_character=0
open_canvas(width, height)



world=[]
background = Background()
current_Map = CurrentMap()
current_Map.change_map(2)
bubbles = []
enemies = []
enemies_balls = []
player_UI=None

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
        #인트로 추가예정
        global Intro_screen
        Intro_screen = intro_screen()
        world.append(Intro_screen)
    if (current_Map.current_map == 2):
        world.clear()

        global player
        global player_UI
        player_UI = Player_UI()
        town = Town()
        world.append(town)

        player = Character(200, 300)
        world.append(player)
        enemy = Enemy('trainer_BURGLAR.png', 900, 400, 1)
        world.append(enemy)

def world_update():
    global current_Map
    if (current_Map.current_map == 0):
        handle_events(player,world,current_Map)
        if current_Map.current_map == 1:
            world_reset()

    if (current_Map.current_map == 1):
        if handle_events(player,world,current_Map) == 'next':
             global Intro_screen
             Intro_screen.dialogue_index+=1
             Intro_screen.text_index=0

        for obj in world:
            #플레이어는 현재맵까지 전달
            if isinstance(obj, Character):
                obj.update(current_Map.current_map)
            else:
                obj.update()

        if Intro_screen.step==7:
            #다음 장면으로 넘어감
            current_Map.change_map(2)
            world_reset()



    if (current_Map.current_map == 2):
        #버블 리턴하게함
        temp_bubble = handle_events(player,world,current_Map)
        player.update_frame()
        if isinstance(temp_bubble, Bubble):
            bubbles.append(temp_bubble)

        for obj in world:
            if isinstance(obj, Character):
                obj.update(current_Map.current_map)
            elif isinstance(obj, Enemy):
                ball = obj.update(player,0.05)
                if ball is not None:
                    world.append(ball)
                    enemies_balls.append(ball)
                    print("볼 생성")

            else:
                obj.update()
        #충돌체크
        collision_player_object(player, enemies_balls,world)

def wolrd_draw():
    global player_UI
    for obj in world:
        obj.draw()
    player_UI.draw(player)



world_reset()
while True:
    clear_canvas()


    world_update()
    wolrd_draw()



    update_canvas()
    delay(0.02)


close_canvas()