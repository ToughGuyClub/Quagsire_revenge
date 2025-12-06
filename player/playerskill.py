from pico2d import *
import game_framework
import game_world
from handleEvent import get_mouse_pos
from play_modes import Thunder_mode
width, height =  1400, 800
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
        self.current_skills = [0,0,0,0]  # 현재 장착된 스킬들
        self.current_unlock_skills = [0,0,0,0] #현재 해금 된 스킬
        self.cur_using_skill = None
        self.skills = {
            1: {  # 1번 슬롯
                     # 레벨 1일 때
                1: WaterCannon,  # 레벨 1일 때
                2: WaterBeam,    # 레벨 2일 때
                3: HyperBeam      # 레벨 3일 때
            },
            2: {
                1: WaterShield,
                2: WaterParrying,
                3: WaterHeal         #체력회복
            },
            3: {
                1: IceSpear,        #얼음창 3개 생성 후 충전 후 발사
                2: EarthQuake,      #해당 벡터로 여러 지진 발사
                3: FLASH,            #hekireki issen
            },
            4: {
                1:METEOR,         #반경 n미터 이내 적에게 낙뢰
                2:HekirekiIssen,         #메테오로 맵 전체 타격
                3: None,
            }
        }
        # 스킬별 쿨타임 설정 (초 단위)
        self.skill_cooltimes = {
            1: 5.0,  # WaterBeam 쿨타임 3초
            2: 5.0,  # WaterCannon 쿨타임 5초
            3: 5.0,  # WaterShield 쿨타임 8초
            4: 10.0,
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
            if isinstance(skill_class,EarthQuake ):
                new_skill = skill_class(self.player,1)
            else:
                new_skill = skill_class(self.player)
            new_skill.use()
            cur_using_skill=new_skill
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
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'water_cannon.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'water_cannon_p.png'))
        self.duration = 1.0  # 지속 3초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=250  #플레이어로부터 떨어진 거리
        self.icon_clip = (0, 0, 85, 120)  # 아이콘 클립좌표
        self.damage=10
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
        self.push_degree=0.0
        print("캐논호출호출")
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('cannon:enemy', self, None)
        game_world.add_object(self, 3)
        print("Water Cannon used!")
    def update(self):
        self.duration -= game_framework.frame_time

        if self.duration <= 0:
            game_world.remove_object(self)
            return
        for enemy in list(self.hit_cooldowns.keys()):
            self.hit_cooldowns[enemy] += game_framework.frame_time
        # 플레이어 방향(8방향)에 따라 방향 설정
        self.dirX, self.dirY = self.player.dirX, self.player.dirY
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy =  last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        self.degree = math.degrees(math.atan2(dy, dx))
        self.push_degree=self.degree
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
        self.x = self.player.x + self.distance/1.5 * math.cos(rad)
        self.y = self.player.y + self.distance/1.5 * math.sin(rad)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        pass
    def draw(self):
        rad = math.radians(self.degree)
        if self.dirX<0:
            self.image.clip_composite_draw(int(self.frame) * 85, 0, 85, 120,
                                           rad - math.pi / 2,  # 기본 이미지가 세로형이라면 -90도 보정
                                           'h',
                                           self.x, self.y,
                                           130, 280)
        else: self.image.clip_composite_draw(int(self.frame) * 85, 0, 85, 120,
                                       rad - math.pi / 2,  # 기본 이미지가 세로형이라면 -90도 보정
                                       '',
                                       self.x, self.y,
                                       130, 280)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False
class WaterBeam:
    def __init__(self,player):
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'water_beam.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'water_beam_p.png'))
        self.duration = 2.0  # 지속 2초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frameX=0.0
        self.frameY=2.0

        self.x=self.player.x
        self.y=self.player.y
        self.distance=500  #플레이어로부터 떨어진 거리
        self.icon_clip = (200, 200, 200, 200)#아이콘 클립좌표
        self.damage=20
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
        self.push_degree=0.0
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('cannon:enemy', self, None)
        game_world.add_object(self, 3)
        print("Water Beam used!")
    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            return
        # 플레이어 방향(8방향)에 따라 방향 설정
        self.dirX, self.dirY = self.player.dirX, self.player.dirY
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy =  last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        self.degree = math.degrees(math.atan2(dy, dx))
        self.push_degree=self.degree
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
        if self.duration>=1.5:
            self.distance=90
            self.x = self.player.x + self.distance*3 * math.cos(rad)
            self.y = self.player.y + self.distance*3 * math.sin(rad)
        else:
            self.distance=500
            self.x = self.player.x + self.distance/2 * math.cos(rad)
            self.y = self.player.y + self.distance/2 * math.sin(rad)

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
                                           500, 240)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class EarthQuake:
    def __init__(self,player,Dx=0,Dy=0,deg=0.0,step=1):
        self.image = load_image(os.path.join('asset/player/skill', 'earth_quake.png'))
        self.duration = 1.0  # 지속 2초
        self.player=player
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y

        self.step=step
        self.distance = 100*(step/5)  # 사거리
        self.icon_clip = (0, 0, 60, 60)  # 아이콘 클립좌표
        self.damage=30
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
        # 플레이어 방향(8방향)에 따라 방향 설정
        self.dirX, self.dirY = self.player.dirX, self.player.dirY
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy = last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        if step==1: self.degree = math.degrees(math.atan2(dy, dx))
        else: self.degree=deg
        self.push_degree=self.degree
        # 플레이어 방향수정
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
        if step==1:
            self.x = self.player.x + self.distance/2 * math.cos(rad)
            self.y = self.player.y + self.distance/2 * math.sin(rad)
        else:
            self.x = Dx + self.distance * math.cos(rad)/2
            self.y = Dy + self.distance * math.sin(rad)/2
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('EQ:enemy', self, None)
        game_world.add_object(self, 1)

    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        self.frame = (self.frame + TIME_PER_ACTION_EARTH_QUAKE * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.duration <= 0.9 and self.step>0and self.step<10:
            #self.player.skill_manager.cooldowns[3] = 0.0
            EarthQuake(self.player, self.x,self.y,self.degree,self.step + 1).use()
            self.step=0

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

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class WaterShield:
    def __init__(self,player):
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'water_sheild.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'water_sheild_p.png'))
        self.duration = 5.0  # 지속 3초
        self.player=player
        self.frameX=0.0
        self.frameY=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=200  #사거리
        self.icon_clip = (100, 100, 100, 100)  # 아이콘 클립좌표
        self.damage=3
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('EQ:enemy', self, None)
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

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class HyperBeam:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'hyper_beam.png'))
        self.duration = 3.0  # 지속 4초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frameX=0.0
        self.frameY=0.0
        self.charged= False

        self.x=self.player.x
        self.y=self.player.y
        self.distance=1500  #플레이어로부터 떨어진 거리
        self.icon_clip = (200, 200, 200, 200)#아이콘 클립좌표
        self.damage=100
        self.hit_interval = 0.5  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
        self.push_degree=0.0
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_object(self, 3)
        print("Water Cannon used!")
    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            return
        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if self.duration >= 2.5:
            self.frameY = 0.0
        elif self.duration > 0.5:
            if self.charged==False:
                game_world.add_collision_pair('cannon:enemy', self, None)
                self.charged=True
            self.frameY = 1.0
        elif self.duration <= 0.5:
            self.frameY = 2.0
        # 플레이어 방향(8방향)에 따라 방향 설정
        self.dirX, self.dirY = self.player.dirX, self.player.dirY
        last_mouse_x, last_mouse_y = get_mouse_pos()
        dx = last_mouse_x - self.player.x
        dy =  last_mouse_y - self.player.y  # y좌표 보정 (pico2d는 아래→위)
        self.degree = math.degrees(math.atan2(dy, dx))
        self.push_degree=self.degree
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
        # 위치 갱신 (플레이어 앞쪽 distance만큼(보정))

        rad = math.radians(self.degree)
        if self.frameY==0.0:
            self.x = self.player.x + self.distance//15 * math.cos(rad)
            self.y = self.player.y + self.distance//15 * math.sin(rad)
        else:
            self.x = self.player.x + self.distance//2.5 * math.cos(rad)
            self.y = self.player.y + self.distance//2.5 * math.sin(rad)

        pass
    def draw(self):
        rad = math.radians(self.degree)


        self.image.clip_composite_draw(int(self.frameX) * 192, int(self.frameY)*192, 192, 192,
                                       rad - math.pi / 2,  # 기본 이미지가 세로형이라면 -90도 보정
                                       'h',
                                       self.x, self.y,
                                       300, 1500)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class WaterParrying:
    def __init__(self,player):
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'water_parrying.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'water_parrying_p.png'))
        self.duration = 0.5  # 지속 1초
        self.player=player
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.distance=200  #사거리
        self.icon_clip = (0, 0, 102, 75)  # 아이콘 클립좌표
        self.damage=0
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('EQ:enemy', self, None)
        game_world.add_object(self, 3)

    def update(self):
        self.duration -= game_framework.frame_time
        self.x = self.player.x
        self.y = self.player.y
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        self.frame = (self.frame + FRAMES_PER_ACTION* ACTION_PER_TIME_WATER_SHIELD * game_framework.frame_time) % 4


    def draw(self):


        self.image.clip_draw(int(self.frame) * 102, 0, 102, 75,
                                           self.x, self.y,
                                           self.distance,self.distance)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        if group=='EQ:enemy':
            self.player.skill_manager.cooldowns[2]=1.0  #워터쉴드 맞으면 쿨타임 초기화
            #이거만 있으면 별로인거같으니 반격기도 만들어야할거같은데
            #현재 플레이어가 장착중인 빔기술 발사(쿨타임 초기화 포함)
            self.player.skill_manager.cooldowns[1]=0.0
            self.player.skill_manager.use_skill(1)
            game_world.remove_collision_object(self)
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass

    def can_damage(self, enemy):
        # interval dict 없다면 생성 → 첫 타 즉시 허용
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = self.hit_interval

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class WaterHeal:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'water_heal.png'))
        self.duration = 1.0 # 지속 1초
        self.player=player
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.heal_count=40
        self.icon_clip = (170, 0, 85, 90)  # 아이콘 클립좌표
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_object(self, 3)

    def update(self):
        self.duration -= game_framework.frame_time
        self.x = self.player.x
        self.y = self.player.y
        if self.heal_count>0:
            self.player.cur_HP= min(self.player.max_HP, self.player.cur_HP + (1))
            self.heal_count-=1
        if self.duration <= 0:
            #만약 프레임문제로 다 힐 못하면 나머지 힐
            if self.heal_count>0:
                self.player.cur_HP= min(self.player.max_HP, self.player.cur_HP + (10*self.heal_count))
            game_world.remove_object(self)
            return
        self.frame = (self.frame + FRAMES_PER_ACTION* ACTION_PER_TIME_WATER_SHIELD * game_framework.frame_time) % 4


    def draw(self):


        self.image.clip_draw(int(self.frame) * 85, 0, 85, 90,
                                           self.x, self.y+20,
                                           100,110)

        pass
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass
    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.0

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False

class IceSpear:
    def __init__(self,player,angle=0.0):
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'ice_spear.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'ice_spear_p.png'))
        self.duration = 4.0  # 지속 4초
        self.player=player
        self.dirX=0
        self.dirY=0
        self.degree=0
        self.frame=0.0
        self.charged= False
        self.sizeX=88
        self.sizeY=16

        self.EXangle=angle
        self.x=self.player.x
        self.y=self.player.y
        self.distance=-100  #플레이어로부터 떨어진 거리
        self.icon_clip = (0, 0, 88, 16)#아이콘 클립좌표
        self.damage=0
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}

    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):

        game_world.add_collision_pair('bubble:enemy', self, None)
        game_world.add_object(self, 3)

    def update(self):
        if self.duration >= 4.0 and self.EXangle==0.0:
            IceSpear(self.player, -20.0).use()
            IceSpear(self.player, 20.0).use()


        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            return
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

        if self.charged==False:
            # 플레이어 방향(8방향)에 따라 방향 설정
            self.dirX, self.dirY = self.player.dirX, self.player.dirY
            last_mouse_x, last_mouse_y = get_mouse_pos()
            dx = last_mouse_x - self.player.x
            dy =  last_mouse_y - self.player.y  # y좌표 보정
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
            # 위치 갱신 (플레이어 앞쪽 distance만큼(보정))
            rad = math.radians(self.degree + self.EXangle)

            self.x = self.player.x + self.distance * math.cos(rad)
            self.y = self.player.y + self.distance * math.sin(rad)
        if self.duration <=3.0:
            self.charged=True
            self.damage=20
            self.push_degree=self.degree +self.EXangle

            rad = math.radians(self.degree +self.EXangle/2)  # 발사 각도(보정 포함)
            # 이동
            self.x += math.cos(rad) * 1000 * game_framework.frame_time
            self.y += math.sin(rad) * 1000 * game_framework.frame_time
            if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
                game_world.remove_object(self)




        pass
    def draw(self):
        rad = math.radians(self.degree)

        if self.EXangle!=0.0:
            self.image.clip_composite_draw(int(self.frame) * 88, 0, 88, 16,
                                       rad - math.pi +math.radians(self.EXangle) ,  # 기본 이미지가 세로형이라면 -90도 보정
                                       'h',
                                       self.x, self.y,
                                       self.sizeX,self.sizeY)
        else:
            self.image.clip_composite_draw(int(self.frame) * 88, 0, 88, 16,
                                       rad - math.pi ,  # 기본 이미지가 세로형이라면 -90도 보정
                                       'h',
                                       self.x, self.y,
                                       self.sizeX,self.sizeY)
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        return self.x - self.sizeX/2, self.y - self.sizeX/2, self.x + self.sizeX/2, self.y + self.sizeX/2

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False


class HekirekiIssen:
    def __init__(self, player ):
        self.image = load_image(os.path.join('asset/player/skill', 'thunder.png'))
        self.icon_clip = (0, 0, 104, 108)  # 아이콘 클립좌표

    def can_use(self, current_time):
        # 쿨타임 체크
        pass

    def use(self):
        game_framework.push_mode(Thunder_mode)  # 낙뢰 모드로 전환
        pass

    def update(self):
        game_world.remove_object(self)
    def draw(self):

        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip

    def get_bb(self):
        pass
class FLASH:
    def __init__(self,player):
        self.image = load_image(os.path.join('asset/player/skill', 'flash.png'))
        self.icon_clip = (0, 0, 256, 256)  # 아이콘 클립좌표
        self.alpha = 0.0  # 현재 알파값 (0~1)
        self.state = "idle"  # idle → fade_in → fade_out
        self.fade_in_speed = 4.0  # 빠르게 흰색으로
        self.fade_out_speed = 1.5  # 천천히 사라짐
        self.active = False
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        self.alpha = 0.0
        self.state = "fade_in"
        self.active = True
        game_world.add_object(self, 4)
        #적들 플래시상태로만들기
        for layer in game_world.world_temporary:
            for o in layer[:]:
                if hasattr(o, 'is_enemy') and (o.is_enemy or o.is_onix):
                    o.flashed=True

    def update(self):
        if not self.active:
            return

            # 1) 빠르게 밝아짐
        if self.state == "fade_in":
            self.alpha += self.fade_in_speed * game_framework.frame_time
            if self.alpha >= 1.0:
                self.alpha = 1.0
                self.state = "fade_out"

            # 2) 천천히 사라짐
        elif self.state == "fade_out":
            self.alpha -= self.fade_out_speed * game_framework.frame_time
            if self.alpha <= 0.0:
                self.alpha = 0.0
                self.active = False
                game_world.remove_object(self)
    def draw(self):
        if not self.active:
            return
        draw_rectangle(0, 0, width, height, 255, 255, 255, int(self.alpha * 255), True)
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        pass
class METEOR:
    def __init__(self,player,stack=0):
        if player.type==1:
            self.image = load_image(os.path.join('asset/player/skill', 'meteor.png'))
        elif player.type==2:
            self.image = load_image(os.path.join('asset/player/skill', 'meteor_p.png'))
        self.image_after = load_image(os.path.join('asset/player/skill', 'meteor_after.png'))
        self.duration = 5.0  # 지속 4초
        self.x=-100
        self.y=-100
        self.target_y=0
        self.frame=0.0
        self.stack=stack
        self.explosion=False
        self.initialized=False
        self.sizeX=300
        self.sizeY=300
        self.player=player
        self.speed=400
        self.icon_clip = (0, 0, 88, 16)#아이콘 클립좌표
        self.damage=0
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}

        if game_world.get_enemy_list_length() > 0:
            tx, ty = game_world.get_enemy_list_y(self.stack)
            if not (tx==-1):

                self.x, self.target_y = tx,ty

                self.y = self.target_y + 500
        elif game_world.get_enemy_list_length() <= 0:
            self.stack = 200
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        game_world.add_collision_pair('bubble:enemy', self, None)
        game_world.add_object(self, 3)

    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration<=4.9:
            #다음 메테오 생성
            if self.stack!=200:
                METEOR(self.player,self.stack+1).use()
                self.stack=200
        if self.duration <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            return
        if self.explosion==False:
           self.y -= self.speed * game_framework.frame_time
        #적과 일정거리가 되면 폭발
        if not self.explosion and abs(self.y - self.target_y) <= 10:
            self.explosion=True
            self.damage=100
            self.frame=0.0

        if self.explosion and int(self.frame)<=3:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        elif self.explosion and int(self.frame)>3:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)

            self.damage=30
            pass


    def draw(self):
        if not self.explosion:
            self.image.clip_draw(int(self.frame) * 98, 0, 98,100,self.x, self.y,self.sizeX,self.sizeY)
        elif self.explosion and int(self.frame)<=3:
            self.image.clip_draw(int(self.frame+1) * 98, 0, 98,100,self.x, self.y,self.sizeX,self.sizeY)
        elif self.explosion and int(self.frame)>3:
            self.image_after.clip_draw(0,0,256,128,self.x, self.y,self.sizeX/2,self.sizeY/2)
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
    def handle_collision(self, group, other):
        pass

    def get_icon_clip(self):
        return self.image, self.icon_clip
    def get_bb(self):
        if self.explosion:
            return self.x - self.sizeX/4, self.y - self.sizeY/4, self.x + self.sizeX/4, self.y + self.sizeY/4
        else:
            return self.x - 1, self.y +1000, self.x+ 1, self.y + 1002

    def can_damage(self, enemy):
        # interval dict 없다면 생성
        if enemy not in self.hit_cooldowns:
            self.hit_cooldowns[enemy] = 0.2

        self.hit_cooldowns[enemy] += game_framework.frame_time

        # 일정 시간 지나면 공격 가능
        if self.hit_cooldowns[enemy] >= self.hit_interval:
            self.hit_cooldowns[enemy] = 0.0
            return True

        return False