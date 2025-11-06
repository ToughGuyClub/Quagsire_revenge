from pico2d import *
from screen.background import Background
from player.character import Character
from player.character import Bubble
from handeEvent import handle_events
from map.town.Town import Town
from current_map import CurrentMap
from screen.mainScreen import main_screen
import screen.intro
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
def init():
    global current_Map


    #world.clear()

    global player
    global player_UI
    player_UI = Player_UI()
    town = Town()
    world.append(town)

    player = Character(200, 300)
    world.append(player)
    enemy = Enemy('trainer_BURGLAR.png', 900, 400, 1)
    world.append(enemy)

def update():
    global current_Map


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

def draw():
    clear_canvas()
    global player_UI
    for obj in world:
        obj.draw()

    player_UI.draw(player)
    update_canvas()

def finish():
    pass
def pause():
    pass
def resume():
    pass
