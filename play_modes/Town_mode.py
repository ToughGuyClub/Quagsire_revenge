from pico2d import *
from screen.background import Background
from player.character import Character
from player.character import Bubble
import handleEvent
from map.town.Town import Town
from current_map import CurrentMap
from screen.mainScreen import main_screen
import screen.intro
from enemy.Enemy import Enemy
from player.player_UI import Player_UI
import game_world
import game_framework
width, height =  1400, 800
frame_character=0
open_canvas(width, height)
from map.town.town_npc import Snorlax



background = Background()

#current_Map.change_map(2)

bubbles = []
enemies = []
enemies_balls = []
snorlax_npc= None
player_UI=None
player = None
current_Map = None
def init():
    global current_Map

    global snorlax_npc
    for layer in game_world.world_npc:
        for o in layer:
            if isinstance(o, Snorlax):
                snorlax_npc = o
    if snorlax_npc is None:
        snorlax_npc = Snorlax()
        game_world.add_npc(snorlax_npc, 0)

    #world.clear()

    global player
    global player_UI
    # persistent layer에서 이미 존재하는 객체를 찾기
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o, Character):
                player = o
            elif isinstance(o, Player_UI):
                player_UI = o
            elif isinstance(o, CurrentMap):
                current_Map = o

    # 혹시 없을 경우에만 새로 생성
    if current_Map is None:
        current_Map = CurrentMap()
        current_Map.current_map = 2
        current_Map.current_map_id = 2
        game_world.add_object(current_Map, 1, True)
    if player is None:
        player = Character(current_Map, 200, 300)
        game_world.add_object(player, 0, True)  # persistent=True로 등록
        game_world.add_collision_pair('player:enemy', player, None)

    if player_UI is None:
        player_UI = Player_UI(player)
        game_world.add_object(player_UI, 1, True)


    town = Town()


    #랜더링에 필요한것
    game_world.add_object(town, 0)

    #세이브로드
    import screen.mainScreen
    if screen.mainScreen.get_load_save():
        player.load()
        handleEvent.load_save=False


def update():
    global current_Map
    game_world.update()

    #버블 리턴하게함
  #  temp_bubble = handle_events(player,world,current_Map)

    #if isinstance(temp_bubble, Bubble):
    #    bubbles.append(temp_bubble)
    snorlax_npc.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    snorlax_npc.draw()
    update_canvas()

def finish():
    pass
def pause():
    pass
def resume():
    pass
def handle_events():
     result = handleEvent.handle_events(player,game_world,current_Map)
    #npc와 상화작용 처리(바운딩박스를 이용해서 F키 입력시 push할 예정)
     if result == 'Snorlax_npc':
         if game_world.collide(player, snorlax_npc):
             import play_modes.Snorlax_npc_mode
             #푸시 전에 플레이어 입력 다 false로 하기
             from player.character import reset_pressed_keys
             reset_pressed_keys()
             game_framework.push_mode(play_modes.Snorlax_npc_mode)
