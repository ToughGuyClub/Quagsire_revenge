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
                #"east":  (3, 100, 400),   # 오른쪽 끝 → 늪지1
                #"east": (9, 100, 400),      #디버깅용 마을->사막
                "east":(19,100,400)      #디버깅용 마을->화산
            },
            3: {
                "west":  (2, 1300, 400),  # 왼쪽 끝 → 마을맵
                "east":  (4, 100, 400),   # 오른쪽 끝 → 늪지2
                "south": (10, 700, 500),   # 아래 끝 → 던전1
            },
            4: {
                "west":  (3, 1300, 400),  # 왼쪽 끝 → 늪지1
                "east":  (5, 100, 400),   # 오른쪽 끝 → 늪지3
                "north": (13, 700, 100),   # 위 끝 → 얼음1
            },
            5:{
                "west":  (4, 1300, 400),  # 왼쪽 끝 → 늪지2
                "east":  (6, 100, 400),   # 오른쪽 끝 → 숲1
            },
            6: {
                "west":  (5, 1300, 400),  # 왼쪽 끝 → 늪지3
                "east":  (7, 100, 400),   # 오른쪽 끝 → 숲2
            },
            7: {
                "west":  (6, 1300, 400),  # 왼쪽 끝 → 숲1
                "east":  (8, 100, 400),   # 오른쪽 끝 → 숲3
            },
            8: {
                "west":  (7, 1300, 400),  # 왼쪽 끝 → 숲2
                "east":  (9, 100, 400),   # 오른쪽 끝 → 웅이(사막)
            },
            9: {
                "west":  (8, 1300, 400),  # 왼쪽 끝 → 숲3
            },
            10: {
                "north": (3, 700, 100),   # 위 끝 → 늪지1
                "east":  (11, 100, 400),   # 오른쪽 끝 → 던전2
            },
            11: {
                "west":  (10, 1300, 400),  # 왼쪽 끝 → 던전1
                "east":  (12, 100, 400),   # 오른쪽 끝 → 던전3
            },
            12: {
                "west":  (11, 1300, 400),  # 왼쪽 끝 → 던전2
            },
            13: {
                "south": (4, 700, 500),   # 아래 끝 → 늪지2
                "east":  (14, 100, 400),   # 오른쪽 끝 → 얼음2
            },
            14: {
                "west":  (13, 1300, 400),  # 왼쪽 끝 → 얼음1
                "east":  (15, 100, 400),   # 오른쪽 끝 → 얼음3
            },
            15: {
                "west":  (14, 1300, 400),  # 왼쪽 끝 → 얼음2
                "east":  (16, 100, 400),   # 오른쪽 끝 → 묘지1
            },
            16: {
                "west":  (15, 1300, 400),  # 왼쪽 끝 → 얼음3
                "east":  (17, 100, 400),   # 오른쪽 끝 → 묘지2
            },
            17: {
                "west":  (16, 1300, 400),  # 왼쪽 끝 → 묘지1
                "east":  (18, 100, 400),   # 오른쪽 끝 → 묘지3
            },
            18: {
                "west":  (17, 1300, 400),  # 왼쪽 끝 → 묘지2
                "east":  (19, 100, 400),   # 오른쪽 끝 → 화산(지우)
            },
            19:{
                "west":  (18, 1300, 400),  # 왼쪽 끝 → 묘지3
            }
        }

    def get_transition(self, current_map_id, direction):
        """다음 맵 정보 반환: (next_map_id, spawn_x, spawn_y)"""
        return self.links.get(current_map_id, {}).get(direction, None)