from pico2d import *
import math, random
import os
import game_world
import game_framework
from enemy.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector


FAR_DIST = 450
MID_DIST = 180
CLOSE_DIST = 120
Onix_dead=False

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
quest_completed=False
class Onix:
    image = None

    def __init__(self,player):
        # 이미지들
        self.image_idle = load_image(os.path.join('asset/enemy/Onix','Idle-Anim.png'))
        self.image_walk = load_image(os.path.join('asset/enemy/Onix','Walk-Anim.png'))
        self.image_shoot = load_image(os.path.join('asset/enemy/Onix','Shoot-Anim.png'))
        self.image_attack = load_image(os.path.join('asset/enemy/Onix','Hop-Anim.png'))
        self.image_hurt = load_image(os.path.join('asset/enemy/Onix','Hurt-Anim.png'))
        self.x, self.y = 800,300
        self.player = player
        self.animations = {
            'idle': (self.image_idle, 0),
            'walk': (self.image_walk, 0),
            'attack': (self.image_attack, 0),
            'shoot': (self.image_shoot, 0),
            'hurt': (self.image_hurt, 0)
        }
        self.state = 'idle'

        # 애니메이션
        self.frameX = 0.0
        self.frameY = 0
        self.dir = 1
        self.speed = 80.0
        self.size = 300

        # 상태(공통)
        self.flashed = False
        self.flash_timer = 0.0
        self.is_hit = False
        self.hit_effect_timer = 0.0
        self.push_degree = 0.0
        self.HP = 1000
        self.max_HP = 1000
        self.alive = True
        self.hp_bar = ONIX_HP(self)
        # 공격 쿨다운 (초)
        self.cool_primitive = 15.0    # 원거리 "원시의 힘"
        self.cool_earthquake = 9.0   # 중거리 "지진"
        self.cool_dash = 5.0         # 근거리 돌진
        self.primitive_timer = 14.0
        self.earth_timer = 8.0
        self.dash_timer = 4.0
        self.is_onix=True
        #스킬상태
        self.action_lock_timer = 0.0  # 스킬 시전 중 움직임 금지 시간

        # 돌진 상태
        self.dashing = False
        self.moving = False
        self.dash_degree = 0.0
        self.dash_remain = 0.0
        self.dash_hit_done = False
        self.hit_timer=2.0
        self.damage = 40 #돌진을 위한것
        # 행동트리 구성
        self.build_behavior_tree()

        game_world.add_object(self, 2)
        #충돌처리용
        game_world.add_collision_pair('player:enemy', None,self )
        game_world.add_collision_pair('bubble:enemy', None, self)
        game_world.add_collision_pair('cannon:enemy', None, self)
        game_world.add_collision_pair('EQ:enemy', None, self)

        game_world.enemy_list.append(self)

    # -------------------------
    # 유틸: 거리/방향
    # -------------------------
    def distance_to_player(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        return math.sqrt(dx*dx + dy*dy)

    def angle_to_player(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        return math.atan2(dy, dx)


    # 원거리 공격(원시의 힘)3번 연속
    def action_primitive_power(self):
        # 쿨다운 체크
        if self.primitive_timer > 0 or self.action_lock_timer > 0:
            return BehaviorTree.FAIL

        for i in range(3):
            sx = (random.random() - 0.5) * 80  # 발사 위치 편차
            sy = ((random.random() - 0.5) * 80)+200
            ACIENTPOWER(self,self.player , sx, sy)

        self.primitive_timer = self.cool_primitive

        self.action_lock_timer = 3.0
        self.state = 'attack'

        return BehaviorTree.SUCCESS

    # 중거리 공격: 지진
    def action_earthquake(self):
        if self.earth_timer > 0 or self.action_lock_timer > 0:
            return BehaviorTree.FAIL

        EarthQuake(self,self.player,0,0,self.angle_to_player())
        EarthQuake(self, self.player, 0, 0, self.angle_to_player()+30.0)
        EarthQuake(self, self.player, 0, 0, self.angle_to_player()-30.0)

        self.earth_timer = self.cool_earthquake

        self.action_lock_timer = 3.0
        self.state = 'attack'

        return BehaviorTree.SUCCESS

    # 근거리 돌진:
    def action_dash(self):
        if self.dashing:
            # 돌진 진행
            speed = 700.0
            move_x = math.cos(self.dash_degree) * speed * game_framework.frame_time
            move_y = math.sin(self.dash_degree) * speed * game_framework.frame_time
            self.x += move_x
            self.y += move_y
            self.dash_remain -= math.sqrt(move_x*move_x + move_y*move_y)
            # 충돌/벽 감지
            if self.dash_remain <= 0:
                # 돌진 종료
                self.dashing = False
                self.hit_timer=0.0
                self.dash_timer = self.cool_dash
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING
        else:
            # 돌진 시작 체크
            if self.dash_timer > 0:
                return BehaviorTree.FAIL
            # 돌진 시작: 각도 저장, 남은 거리 설정
            self.dash_degree = self.angle_to_player()
            self.dash_remain = 240  # 돌진 총거리(조정)
            self.dashing = True
            self.dash_hit_done = False
            self.hit_timer=0.2
            return BehaviorTree.RUNNING

    # 기본 공격: 이동하면서 연속으로 발사
    def action_basic_attack(self):

        if not hasattr(self, 'basic_timer'):
            self.basic_timer = 0.0
        self.basic_timer -= game_framework.frame_time
        if self.basic_timer <= 0:
            # 발사
            dx = self.player.x - self.x
            dy = self.player.y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist != 0:
                dirX = dx / dist
                dirY = dy / dist
            else:
                dirX, dirY = 0, 0

            ball = AttackBall(

                self.x,
                self.y,
                dirX,
                dirY,
                speed=10,
            )
            game_world.add_object(ball, 2)
            game_world.add_collision_pair('player:enemy', None, ball)
            game_world.add_collision_pair('EQ:enemy', None, ball)

            self.basic_timer = 2.5  # 기본공격 빈도 조절

        return BehaviorTree.SUCCESS

    # 이동 액션: 플레이어 쪽으로 천천히 이동
    def action_move_towards(self):
        self.moving=False
        # 돌진 중이면 이동을 막음(돌진 액션이 우선될 것)
        if self.dashing:
            return BehaviorTree.RUNNING
        # 거리 유지 로직: 너무 가까우면 뒤로 물러남
        dist = self.distance_to_player()
        angle = self.angle_to_player()
        if dist < 130:  # 너무 가까우면 뒷걸음
            back_speed = 80.0
            self.x -= math.cos(angle) * back_speed * game_framework.frame_time
            self.y -= math.sin(angle) * back_speed * game_framework.frame_time
        else:
            # 보통 이동
            self.x += math.cos(angle) * self.speed * game_framework.frame_time
            self.y += math.sin(angle) * self.speed * game_framework.frame_time
        self.moving=True
        return BehaviorTree.SUCCESS


    def cond_far(self):
        return BehaviorTree.SUCCESS if self.distance_to_player() > FAR_DIST else BehaviorTree.FAIL

    def cond_mid(self):
        d = self.distance_to_player()
        return BehaviorTree.SUCCESS if MID_DIST < d <= FAR_DIST else BehaviorTree.FAIL

    def cond_close(self):
        d = self.distance_to_player()
        return BehaviorTree.SUCCESS if d <= CLOSE_DIST else BehaviorTree.FAIL


    def build_behavior_tree(self):
        # 원거리 시퀀스: (원거리 조건 -> 원시의힘 액션)
        far_seq = Sequence('FarSequence',
                           Condition('IsFar', self.cond_far),
                           Action('PrimitivePower', self.action_primitive_power))

        # 중거리: (중거리 조건 -> 지진 액션 ->>기본공격)
        mid_seq = Sequence('MidSequence',
                           Condition('IsMid', self.cond_mid),
                           Action('EarthQuake', self.action_earthquake),
                           Action('BasicAttack', self.action_basic_attack))

        # 근거리: (근거리 조건 -> dash 액션)
        close_seq = Sequence('CloseSequence',
                             Condition('IsClose', self.cond_close),
                             Action('Dash', self.action_dash))


        move_and_attack_seq = Sequence('MoveAndAttack',
                                       Action('Move', self.action_move_towards),
                                       Action('BasicAttack', self.action_basic_attack))

        root_selector = Selector('RootSelector', far_seq, mid_seq, close_seq, move_and_attack_seq)
        self.bt = BehaviorTree(root_selector)


    # 업데이트
    def update(self):
        # 타이머 감소
        dt = game_framework.frame_time
        if self.primitive_timer > 0:
            self.primitive_timer -= dt
        if self.earth_timer > 0:
            self.earth_timer -= dt
        if self.dash_timer > 0:
            self.dash_timer -= dt
        #히트 업데이트
        if self.is_hit:
            self.hit_effect_timer -= dt
            if self.hit_effect_timer <= 0:
                self.is_hit = False

        # 프레임 업데이트
        FRAMES_PER_ACTION = 4
        if self.state == 'idle' or self.state == 'walk':
            FRAMES_PER_ACTION = 4

        elif self.state == 'attack' or self.state == 'shoot':
            FRAMES_PER_ACTION = 10
        elif self.state == 'hurt':
            FRAMES_PER_ACTION = 2


        self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        self.set_frameY()
        # 스킬 시전 타이머 감소
        if self.action_lock_timer > 0:
            self.action_lock_timer -= dt
            self.state = 'attack'

            # *** 시전 중에는 행동 트리를 멈춘다 ***
            return
        if  self.is_hit:
            self.state = 'hurt'
            return
            # 행동 트리 실행
        self.bt.run()
        print(self.animations)
        if self.dashing:
            self.state = 'attack'
        elif self.is_hit:
            self.state = 'hurt'
        elif self.moving:
            self.state = 'walk'
        else:
            self.state = 'idle'

    def draw_half(self):
        from screen.thunder_scene import get_half_stack
        step = get_half_stack()

        # 현재 보스 상태별 이미지와 프레임 크기 가져오기
        if self.state in ('walk', 'idle'):
            image = self.image_walk
            frame_width = 88
            frame_height = 112

        elif self.state == 'attack':
            image = self.image_attack
            frame_width = 88
            frame_height = 160

        elif self.state == 'hurt':
            image = self.image_hurt
            frame_width = 80
            frame_height = 88

        else:
            # 혹시 모르는 예외방지: 기본 idle
            image = self.image_walk
            frame_width = 88
            frame_height = 112

        fx = int(self.frameX) * frame_width
        fy = int(self.frameY) * frame_height

        # -------------------------
        #  상체(위쪽 절반)
        # -------------------------
        image.clip_draw(
            fx,
            fy + frame_height//2,  # y 오프셋
            frame_width,
            frame_height // 2,  # 절반만
            self.x + step,  # 오른쪽 이동
            self.y + self.size * 0.25,  # 살짝 위
            self.size,
            (self.size + self.size // 4) / 2
        )

        # -------------------------
        #  하체(아래쪽 절반)
        # -------------------------
        image.clip_draw(
            fx,
            fy,
            frame_width,
            frame_height // 2,
            self.x - step,  # 왼쪽 이동
            self.y - self.size * 0.25,  # 살짝 아래
            self.size,
            (self.size + self.size // 4) / 2
        )

    def draw(self):
        image, frameY = self.animations.get(self.state, self.animations['idle'])
        frameY = self.frameY
        if self.state == 'walk' or self.state=='idle':
            frame_width = 88
            frame_height = 112

            self.image_walk.clip_draw(int(self.frameX) * frame_width,
                                      frameY * frame_height,
                                      frame_width,
                                      frame_height,
                                      self.x,
                                      self.y,
                                      self.size,
                                      self.size + self.size // 4)
        elif self.state=='attack':
            frame_width = 88
            frame_height = 160
            self.image_attack.clip_draw(int(self.frameX) * frame_width,
                            frameY * frame_height,
                            frame_width,
                            frame_height,
                            self.x,
                            self.y,
                            self.size,
                            self.size + self.size // 4)
        elif self.state=='hurt':
            frame_width = 80
            frame_height = 88
            self.image_hurt.clip_draw(int(self.frameX) * frame_width,
                            frameY * frame_height,
                            frame_width,
                            frame_height,
                            self.x,
                            self.y,
                            self.size*0.8,
                            self.size + self.size // 6)




    def get_bb(self):
        return (self.x - self.size//4, self.y - self.size//6,
                self.x + self.size//4, self.y + (self.size + self.size//5)//2)
    def set_frameY(self):
        #각도계산
        angle = self.angle_to_player()
        angle = math.degrees(angle)
        angle = (angle + 360) % 360

        if 0<=angle<45:
            self.frameY=5
        elif 45<=angle<90:
            self.frameY=4
        elif 90<=angle<135:
            self.frameY=3
        elif 135<=angle<=180:
            self.frameY=2
        elif 180<=angle<225:
            self.frameY=1
        elif 225<=angle<270:
            self.frameY=0
        elif 270<=angle<315:
            self.frameY=7
        elif 315<=angle<360:
            self.frameY=6


    def handle_collision(self, group, other):
        ishit = False
        if group in ('bubble:enemy', 'cannon:enemy', 'EQ:enemy'):
            # self.HP -= 1 * other.damage
            damage = getattr(other, "damage", 0)
            hit_interval = getattr(other, "hit_interval", None)

            # --- 즉발 스킬(버블 등) ---
            if hit_interval is None:
                self.HP -= damage
                ishit = True
                print(f"Enemy HP: {self.HP}")
            else:

                if hasattr(other, "can_damage") and other.can_damage(self):
                    self.HP -= damage
                    ishit = True
                    # 디버깅용 몬스터 객체랑 현재 체력표시
                    print(f"Enemy HP: {self.HP}")
        if ishit:
            self.is_hit = True
            self.hit_effect_timer = 0.3
            # 넉백 각도 설정
            dx = self.x - other.x
            dy = self.y - other.y
            self.push_degree = math.atan2(dy, dx)
        if self.HP <= 0:
            DEATHEFFECTENEMY(self.x, self.y)
            # 퀘스트를 위해 있는 부분
            import map.desert.desert_dialogue
            global Onix_dead
            Onix_dead=True
            from player.character import reset_pressed_keys
            global quest_completed
            quest_completed=True
            reset_pressed_keys()
            game_framework.push_mode(map.desert.desert_dialogue)
            self.player.quest_manager.check_progress(98)
            game_world.remove_object(self.hp_bar)
            game_world.enemy_list.remove(self)
            game_world.remove_object(self)

        pass
class ACIENTPOWER:
    def __init__(self,enemy,player,sx,sy,step=1):
        self.image = load_image(os.path.join('asset/enemy', 'boldore_skill.png'))
        self.enemy=enemy
        self.x = enemy.x
        self.y = enemy.y
        self.sx = sx
        self.sy = sy
        self.dirX = None
        self.dirY = None
        self.speed = 13
        self.scale = 96
        self.frame = 0.0
        self.damage = 5 * 4 * 1.5
        self.player = player
        self.active = False
        self.activation_timer = 1.0  # 발동 대기 시간
        self.push_degree = 0.0
        self.step=step
        #월드에 넣기
        game_world.add_object(self, 4)
        game_world.add_collision_pair('player:enemy', None, self)
        #game_world.add_collision_pair('EQ:enemy', None, self)
    def update(self):
        self.activation_timer -= game_framework.frame_time
        self.frame= (self.frame + 4.0 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.activation_timer >=0.0:
            self.x=self.enemy.x +self.sx
            self.y=self.enemy.y +self.sy

        elif self.activation_timer <0.0:
            #플레이어 방향으로 직선 이동
            if self.dirX is None and self.dirY is None:
                #step에 따라 3번까지 생성
                if self.step<3:
                    #sx랑 sy 다시설정
                    sx= (random.random() - 0.5) * 100  # 발사 위치 편차
                    sy= ((random.random() - 0.5) * 80)+200
                    ACIENTPOWER(self.enemy,self.player, sx, sy, self.step+1)

                    self.step=5

                #방향
                dx = self.player.x - self.x
                dy = self.player.y - self.y
                self.push_degree = math.degrees(math.atan2(dy, dx))
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist != 0:
                    self.dirX, self.dirY = dx / dist, dy / dist
                else:
                    self.dirX, self.dirY = 0, 0
            self.x += self.dirX * self.speed * game_framework.frame_time * self.speed * 5.0
            self.y += self.dirY * self.speed * game_framework.frame_time * self.speed * 5.0

        #경계처리
        if self.x < 0 or self.x > 1600 or self.y < 0 or self.y > 900:
            game_world.remove_object(self)
    def draw(self):
        if self.activation_timer >= 0:
            self.image.clip_draw(int(self.frame), 0, 192,192 , self.x, self.y, self.scale*2,  self.scale*2)

        elif self.activation_timer < 0:
            self.image.clip_draw(int(self.frame), 192, 192, 192, self.x, self.y, self.scale*2, self.scale*2)

    def get_bb(self):
        return self.x - self.scale/2 , self.y - self.scale/2 , self.x + self.scale/2 , self.y + self.scale/2
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
        elif group == 'EQ:enemy':
            game_world.remove_object(self)


class EarthQuake:
    def __init__(self,player,target,Dx=0,Dy=0,deg=0.0,step=1):
        self.image = load_image(os.path.join('asset/player/skill', 'earth_quake.png'))
        self.duration = 1.0  # 지속 2초
        self.player=player
        self.frame=0.0
        self.x=self.player.x
        self.y=self.player.y
        self.target=target
        self.tx=target.x
        self.ty=target.y
        self.step=step
        self.distance = 100*(step/5)  # 사거리
        self.icon_clip = (0, 0, 60, 60)  # 아이콘 클립좌표
        self.damage=20
        self.hit_interval = 0.2  # 적당한 데미지 주기
        self.hit_cooldowns = {}  # {enemy_obj : elapsed_time}
        self.is_eq = True
        # 플레이어 방향(8방향)에 따라 방향 설정
        game_world.add_collision_pair('player:enemy', None, self)
        last_mouse_x, last_mouse_y = self.tx,self.ty
        dx = last_mouse_x - self.x
        dy = last_mouse_y - self.y  # y좌표 보정 (pico2d는 아래→위)
        if step==1: self.degree = math.degrees(math.atan2(dy, dx))+deg
        else: self.degree=deg
        self.push_degree=self.degree

        # 위치 갱신 (플레이어 앞쪽 distance만큼)
        rad = math.radians(self.degree)
        if step==1:
            self.x = self.x + self.distance/2 * math.cos(rad)
            self.y = self.y + self.distance/2 * math.sin(rad)
        else:
            self.x = Dx + self.distance * math.cos(rad)/2
            self.y = Dy + self.distance * math.sin(rad)/2
        game_world.add_object(self, 3)
    def can_use(self, current_time):
        #쿨타임 체크
        pass

    def use(self):
        #game_world.add_collision_pair('EQ:enemy', self, None)
        pass

    def update(self):
        self.duration -= game_framework.frame_time
        if self.duration <= 0:
            game_world.remove_object(self)
            return
        self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
        if self.duration <= 0.9 and self.step>0and self.step<10:
            #self.player.skill_manager.cooldowns[3] = 0.0
            EarthQuake(self.player,self.target, self.x,self.y,self.degree,self.step + 1).use()
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
        half_size = self.distance / 4
        return (self.x - half_size, self.y - half_size,
                self.x + half_size, self.y + half_size)

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


class AttackBall:
    def __init__(self, x, y, dirX, dirY ,speed=10 ):
        self.image = load_image(os.path.join('asset/enemy/Onix','basic_attack.png'))
        self.x = x
        self.y = y
        self.dirX = dirX
        self.dirY = dirY
        self.damage = 5*6*1.5
        self.speed = speed
        self.scale = 64
        self. frame = 0
        self.level = 20
        self.frame_time = 0.1
        self.push_degree= math.degrees(math.atan2(dirY, dirX))
    def update(self):
        self.x += self.dirX * self.speed*game_framework.frame_time* self.speed*5.0
        self.y += self.dirY * self.speed*game_framework.frame_time* self.speed*5.0


        #경계처리
        if self.x < 0 or self.x > 1600 or self.y < 0 or self.y > 900:
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(self.frame * 192, 0, 192, 192, self.x, self.y, self.scale,self.scale)

    def get_bb(self):
        return self.x - self.scale/4 , self.y - self.scale/4 , self.x + self.scale/4 , self.y + self.scale/4
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
        elif group == 'EQ:enemy':
            game_world.remove_object(self)

class ONIX_HP:
    def __init__(self, onix):
        self.onix = onix
        if not hasattr(self, 'font'):
            self.font = load_font('asset/screen/intro/introFont.ttf', 20)
        game_world.add_object(self, 4)
        self.state=self.onix.state
    def update(self):
        pass

    def draw(self):
        # HP 바 배경 (폭 400)
        draw_rectangle(800, 750, 1200, 780, 255, 0, 0, 255, True)

        # HP 바
        hp_ratio = self.onix.HP / self.onix.max_HP
        hp_width = 400 * hp_ratio
        draw_rectangle(800, 750, 800 + hp_width, 780, 0, 255, 0, 255, True)

        # HP 텍스트
        hp_text = f"Onix HP: {self.onix.HP} / {self.onix.max_HP}"
        state_text = f"State: {self.onix.state}"

        self.font.draw(900, 785, hp_text, (255, 255, 255))


class DEATHEFFECTENEMY:
    def __init__(self, x, y ):
        self.image = load_image(os.path.join('asset/enemy', 'normal_death.png'))
        self.x = x
        self.y = y
        self.scale = 64
        self.frame = 0.0


        game_world.add_object(self, 4)
    def update(self):
        self.frame = (self.frame + 4.0 * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame >=4:
            game_world.remove_object(self)


    def draw(self):
        self.image.clip_draw(int(self.frame)*68, 0, 68,91 , self.x, self.y, self.scale,  self.scale*2)



def get_quest_type():
    return quest_completed


def check_onix_dead():
    return Onix_dead