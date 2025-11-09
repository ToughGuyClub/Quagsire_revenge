from pico2d import *

width, height = 1400, 800
class CurrentMap:
    def __init__(self):
        self.current_map = 0
    def change_map(self, new_map):
        self.current_map = new_map
    def get_current_map(self):
        return self.current_map
    def update(self):
        pass
    def draw(self):
        pass

class MapConnection:
    def __init__(self):
        # current_map_id : {"direction": (next_map_id, spawn_x, spawn_y)}
        self.links = {
            2: {  # Town Map
                "east":  (4, 100, 400),   # 오른쪽 끝 → 숲맵
            },
            3: {

            },
            4: {

            }
        }

    def get_transition(self, current_map_id, direction):
        """다음 맵 정보 반환: (next_map_id, spawn_x, spawn_y)"""
        return self.links.get(current_map_id, {}).get(direction, None)