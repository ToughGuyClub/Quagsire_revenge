from pico2d import *

import handleEvent
import game_world
width, height =  1400, 800
from map.prairie.prairie import PRAIRIE01, PRAIRIE02
from current_map import CurrentMap
from player.character import Character
player = None
current_Map = None
field_map = None
def init():
    global player, current_Map, field_map

    # 이미 game_world에 persistent 객체로 등록되어 있으므로 다시 생성 안 함
    # 단, 가져와서 참조만 걸어줌
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o,Character):  # 예시) Character 클래스에 player_flag=True 넣어두면 탐색 가능
                player = o
            if isinstance(o, CurrentMap):
                current_Map = o

    # 새 맵 불러오기
    if current_Map.current_map_id==3:
        field_map = PRAIRIE01(player)
    elif current_Map.current_map_id==4:
        field_map = PRAIRIE02(player)
    game_world.add_object(field_map, 0)  # 맵은 일시적 객체

    #상호작용에 필요한 것

def update():

    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass
def pause():
    pass
def resume():
    pass
def handle_events():
    handleEvent.handle_events(player,game_world,current_Map)
    pass


