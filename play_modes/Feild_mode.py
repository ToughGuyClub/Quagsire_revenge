from pico2d import *

import handleEvent
import game_world
width, height =  1400, 800
from map.prairie.prairie import PRAIRIE01, PRAIRIE02, PRAIRIE03
from map.forest.forest import FOREST01, FOREST02, FOREST03
from map.dungeon.dungeon import DUNGEON01, DUNGEON02, DUNGEON03
from map.glacier.glacier import GLACIER01, GLACIER02, GLACIER03
from map.cemetery.cemetery import CEMETERY01, CEMETERY02, CEMETERY03
from map.desert.desert import DESERT
from map.volcano.volcano import VOLCANO
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
                game_world.add_collision_pair('player:enemy', player, None)
            if isinstance(o, CurrentMap):
                current_Map = o

    # 새 맵 불러오기
    if current_Map.current_map_id==3:
        field_map = PRAIRIE01(player)
    elif current_Map.current_map_id==4:
        field_map = PRAIRIE02(player)
    elif current_Map.current_map_id==5:
        field_map = PRAIRIE03(player)
    elif current_Map.current_map_id==6:
        field_map = FOREST01(player)
    elif current_Map.current_map_id==7:
        field_map = FOREST02(player)
    elif current_Map.current_map_id==8:
        field_map = FOREST03(player)
    elif current_Map.current_map_id==9:
        field_map = DESERT(player)
    elif current_Map.current_map_id==10:
        field_map = DUNGEON01(player)
    elif current_Map.current_map_id==11:
        field_map = DUNGEON02(player)
    elif current_Map.current_map_id==12:
        field_map = DUNGEON03(player)
    elif current_Map.current_map_id==13:
        field_map = GLACIER01(player)
    elif current_Map.current_map_id==14:
        field_map = GLACIER02(player)
    elif current_Map.current_map_id==15:
        field_map = GLACIER03(player)
    elif current_Map.current_map_id==16:
        field_map = CEMETERY01(player)
    elif current_Map.current_map_id==17:
        field_map = CEMETERY02(player)
    elif current_Map.current_map_id==18:
        field_map = CEMETERY03(player)
    elif current_Map.current_map_id==19:
        field_map = VOLCANO(player)

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


