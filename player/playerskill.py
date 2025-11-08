from pico2d import *
import game_framework
import game_world
from handleEvent import last_mouse_x, last_mouse_y
height=800
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
class PlayerSkillManager:
    def __init__(self, player):
        self.player = player
        self.timer=2.0
        self.current_skills = {1,1,1,1}  # 현재 장착된 스킬들
        self.skills = {
            1: {  # 1번 슬롯
                1: WaterCannon(player),       # 레벨 1일 때

            },
            2: {
                1: None,
                2: None,
                3: None
            },
            3: {},
            4: {}
        }
    def use_skill(self, slot_number):
        skill_level = 1
        skill = self.skills.get(slot_number, {}).get(skill_level, None)
        if skill:
            skill.use()
        else:
            print(f"No skill equipped in slot {slot_number} at level {skill_level}.")
    def update(self):
        #스킬 시전시간관리 다 끝나면 exit을 위해서임
        self.timer-=game_framework.frame_time

class WaterCannon:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'water_cannon.png'))
        self.duration = 1.0  # 지속 3초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=120  #플레이어로부터 떨어진 거리
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_object(self, 3)
        print("Water Cannon used!")
    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        # 플레이어 방향(8방향)에 따라 방향 설정
        self.dirX, self.dirY = self.player.dirX, self.player.dirY
        # dirX, dirY로 회전 각도 계산 (라디안 → 도)
        self.degree = math.degrees(math.atan2(self.dirY, self.dirX)) if not (self.dirX == 0 and self.dirY == 0) else 0

        # 8방향 보정 (정확히 위/아래/좌/우 등일 때)
        if self.dirX == 0 and self.dirY > 0:
            self.degree = 90
        elif self.dirX == 0 and self.dirY < 0:
            self.degree = -90
        elif self.dirX > 0 and self.dirY == 0:
            self.degree = 0
        elif self.dirX < 0 and self.dirY == 0:
            self.degree = 180
        elif self.dirX > 0 and self.dirY > 0:
            self.degree = 45
        elif self.dirX < 0 and self.dirY > 0:
            self.degree = 135
        elif self.dirX > 0 and self.dirY < 0:
            self.degree = -45
        elif self.dirX < 0 and self.dirY < 0:
            self.degree = -135
        rad = math.radians(self.degree)
        self.x = self.player.x + self.distance * math.cos(rad)
        self.y = self.player.y + self.distance * math.sin(rad)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        pass
    def draw(self):
        rad = math.radians(self.degree)
        if self.dirX<0:
            self.image.clip_composite_draw(int(self.frame) * 85, 0, 85, 120,
                                           rad - math.pi / 2,  # 기본 이미지가 세로형이라면 -90도 보정
                                           'h',
                                           self.x, self.y,
                                           127, 240)
        else: self.image.clip_composite_draw(int(self.frame) * 85, 0, 85, 120,
                                       rad - math.pi / 2,  # 기본 이미지가 세로형이라면 -90도 보정
                                       '',
                                       self.x, self.y,
                                       127, 240)
        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass
    def get_bb(self):
        pass
