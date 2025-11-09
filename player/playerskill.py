from pico2d import *
import game_framework
import game_world
from handleEvent import get_mouse_pos
height=800
TIME_PER_ACTION = 0.5
TIME_PER_ACTION_EARTH_QUAKE = 1.0/0.5

TIME_PER_ACTION_WATER_SHEILD = 0.5
ACTION_PER_TIME_WATER_SHIELD = 1.0 / TIME_PER_ACTION_WATER_SHEILD

ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
class PlayerSkillManager:
    def __init__(self, player):
        self.player = player
        self.timer=2.0
        self.current_skills = [1,1,1,1]  # 현재 장착된 스킬들
        self.skills = {
            1: {  # 1번 슬롯
                     # 레벨 1일 때
               1: WaterBeam,         # 레벨 2일 때

            },
            2: {
                1: WaterCannon,
                2: None,
                3: None
            },
            3: {
                #1: EarthQuake,
                1: WaterShield,
                2: None,
                3: None
            },
            4: {}
        }
        # 스킬별 쿨타임 설정 (초 단위)
        self.skill_cooltimes = {
            1: 3.0,  # WaterBeam 쿨타임 3초
            2: 5.0,  # WaterCannon 쿨타임 5초
            3: 8.0,  # WaterShield 쿨타임 8초
            4: 0.0,
        }

        # 현재 남은 쿨타임 (0이면 사용 가능)
        self.cooldowns = {
            1: 0.0,
            2: 0.0,
            3: 0.0,
            4: 0.0,
        }
    def use_skill(self, slot_number):
        """스킬 사용 시도"""
        # 1쿨타임 체크
        if self.cooldowns[slot_number] > 0:
            print(f"Skill {slot_number} is cooling down: {self.cooldowns[slot_number]:.1f}s left")
            return  # 쿨타임 중이라면 사용 불가

        # 2 스킬 정보 가져오기
        skill_level = self.current_skills[slot_number - 1]
        skill_class = self.skills.get(slot_number, {}).get(skill_level, None)

        if skill_class:
            new_skill = skill_class(self.player)
            new_skill.use()

            # 3 쿨타임 시작
            self.cooldowns[slot_number] = self.skill_cooltimes[slot_number]
            print(f"Skill {slot_number} used! Cooldown started ({self.skill_cooltimes[slot_number]}s)")
        else:
            print(f"No skill equipped in slot {slot_number} at level {skill_level}.")
    def update(self):
        dt = game_framework.frame_time
        for slot in self.cooldowns:
            if self.cooldowns[slot] > 0:
                self.cooldowns[slot] = max(0.0, self.cooldowns[slot] - dt)

        # 기존 타이머 로직
        self.timer -= dt

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
        game_world.add_collision_pair('cannon:enemy', self, None)
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
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy =  last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        self.degree = math.degrees(math.atan2(dy, dx))
        #플레이어 방향수정
        if abs(dx) < 10 and abs(dy) < 10:
            pass  # 너무 가까우면 방향 유지
        else:
            # atan2는 라디안 기준 → 방향을 정규화해서 -1, 0, 1 중 가장 가까운 값으로 설정
            if dx > 10:
                self.player.dirX = 1
            elif dx < -10:
                self.player.dirX = -1
            else:
                self.player.dirX = 0

            if dy > 10:
                self.player.dirY = 1
            elif dy < -10:
                self.player.dirY = -1
            else:
                self.player.dirY = 0
        # 위치 갱신 (플레이어 앞쪽 distance만큼)
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
class WaterBeam:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'water_beam.png'))
        self.duration = 2.0  # 지속 2초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frameX=0.0
        self.frameY=2.0

        self.x=self.player.x
        self.y=self.player.y
        self.distance=120  #플레이어로부터 떨어진 거리
        game_world.add_collision_pair('cannon:enemy', self, None)
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
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy =  last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        self.degree = math.degrees(math.atan2(dy, dx))
        #플레이어 방향수정
        if abs(dx) < 10 and abs(dy) < 10:
            pass  # 너무 가까우면 방향 유지
        else:
            # atan2는 라디안 기준 → 방향을 정규화해서 -1, 0, 1 중 가장 가까운 값으로 설정
            if dx > 10:
                self.player.dirX = 1
            elif dx < -10:
                self.player.dirX = -1
            else:
                self.player.dirX = 0

            if dy > 10:
                self.player.dirY = 1
            elif dy < -10:
                self.player.dirY = -1
            else:
                self.player.dirY = 0
        # 위치 갱신 (플레이어 앞쪽 distance만큼)
        rad = math.radians(self.degree)
        self.x = self.player.x + self.distance * math.cos(rad)
        self.y = self.player.y + self.distance * math.sin(rad)

        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.frameX >= 3 and self.frameY==2:
            self.frameY = (self.frameY - 1)
        if self.duration<=0.5:
            self.frameY=0
        pass
    def draw(self):
        rad = math.radians(self.degree)

        self.image.clip_composite_draw(int(self.frameX) * 200, int(self.frameY)*200, 200, 200,
                                           rad ,  # 기본 이미지가 세로형이라면 -90도 보정
                                           '',
                                           self.x, self.y+20,
                                           250, 240)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        pass
class EarthQuake:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'earth_quake.png'))
        self.duration = 5.0  # 지속 3초
        self.player=player
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=400  #사거리
        game_world.add_collision_pair('EQ:enemy', self, None)
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_object(self, 3)

    def update(self):
        self.duration -= game_framework.frame_time
        self.x = self.player.x
        self.y = self.player.y
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        self.frame = (self.frame + TIME_PER_ACTION_EARTH_QUAKE * ACTION_PER_TIME * game_framework.frame_time) % 2

        if(self.duration<=3.0):
            self.distance=500
        elif(self.duration<=2.0):
            self.distance=800
        pass
    def draw(self):


        self.image.clip_draw(int(self.frame) * 60, 0, 60, 60,
                                           self.x, self.y,
                                           self.distance,self.distance)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        pass
class WaterShield:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'water_sheild.png'))
        self.duration = 5.0  # 지속 3초
        self.player=player
        self.frameX=0.0
        self.frameY=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=200  #사거리
        game_world.add_collision_pair('EQ:enemy', self, None)
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_object(self, 3)

    def update(self):
        self.duration -= game_framework.frame_time
        self.x = self.player.x
        self.y = self.player.y
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        self.frameX = (self.frameX + FRAMES_PER_ACTION* ACTION_PER_TIME_WATER_SHIELD * game_framework.frame_time) % 4
        if self.duration>=4.5:
            self.frameY=0.0
        elif self.duration>=3.0:
            self.frameY=1.0
        elif self.duration<=0.5:
            self.frameY=2.0

    def draw(self):


        self.image.clip_draw(int(self.frameX) * 100, int(self.frameY)*100, 100, 100,
                                           self.x, self.y,
                                           self.distance,self.distance)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_bb(self):
        pass
