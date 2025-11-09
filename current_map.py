from pico2d import *
import game_framework
import game_world

width, height = 1400, 800
class CurrentMap:
    def __init__(self):
        self.current_map = 0
        self.current_map_id = None
        self.map_conn = MapConnection()
    def change_map(self, new_map_id):
        #self.current_map[self.current_map_id].on_exit()  # 현재 맵 나가기
        game_world.clear_temporary()
        self.current_map_id = new_map_id
        import play_modes.Town_mode
        import play_modes.Feild_mode
        if new_map_id == 2:  # Town
            game_framework.change_mode(play_modes.Town_mode)
        else:  # Field
            game_framework.change_mode(play_modes.Feild_mode)



    def get_current_map(self):
        # 항상 현재 맵의 id를 반환하도록 통일
        return self.current_map_id

    def get_transition(self, direction):
        # 편의 메서드: 현재 맵 id를 넣어서 map_conn에게 위임
        return self.map_conn.get_transition(self.current_map_id, direction)

    def update(self):
        pass
    def draw(self):
        pass

class MapConnection:
    def __init__(self):
        # current_map_id : {"direction": (next_map_id, spawn_x, spawn_y)}
        self.links = {
            2: {  # Town Map
                "east":  (3, 100, 400),   # 오른쪽 끝 → 숲맵
            },
            3: {
                "west":  (2, 1300, 400),  # 왼쪽 끝 → 마을맵
                "east":  (4, 100, 400),   # 오른쪽 끝 → 산맵
            },
            4: {
                "west":  (3, 1300, 400),  # 왼쪽 끝 → 숲맵
            }
        }

    def get_transition(self, current_map_id, direction):
        """다음 맵 정보 반환: (next_map_id, spawn_x, spawn_y)"""
        return self.links.get(current_map_id, {}).get(direction, None)