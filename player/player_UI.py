

from pico2d import *

from player.playerskill import PlayerSkillManager
class Player_UI:
    def __init__(self,player):
        self.HP_bar_img = load_image(os.path.join('asset/player','hp_bar.png'))
        self.player = player
    def draw(self ):
        self.draw_health_bar(self.player)
        self.draw_skill_cooldown(self.player)
        pass
    def draw_health_bar(self,player):
        bar_width = 400
        bar_height = 20
        bar_color = 2
        #체력비율에 따라 색깔 바꿈 50%이상 초록 50%미만 노랑 20%미만 빨강
        health_ratio = player.cur_HP / player.max_HP

        if health_ratio > 0.5: bar_color = 2
        elif health_ratio > 0.2: bar_color = 1
        else: bar_color = 0
        self.HP_bar_img.clip_draw(0, bar_color * 6, 96, 6, 250, 750, bar_width * health_ratio, bar_height)
    def draw_exp_bar(self,player):
        pass
    def draw_level(self,player):
        pass

    def draw_skill_cooldown(self, player):
        if not hasattr(self, 'font'):
            self.font = load_font('asset/screen/intro/introFont.ttf', 30)

        skill_size = 64
        spacing = 10
        start_x = 100
        start_y = 100

        # 안전 검사
        if not hasattr(player, 'skill_manager'):
            return
        sm = player.skill_manager

        # 4개의 슬롯을 순회
        for slot in range(1, 5):
            x = start_x + (skill_size + spacing) * (slot - 1)
            y = start_y

            # 현재 슬롯의 스킬 가져오기
            skill_level = sm.current_skills[slot - 1] if slot - 1 < len(sm.current_skills) else 0
            if skill_level == 0:
                continue  # 슬롯에 스킬 없음 → 안 그림

            skill_class = sm.skills.get(slot, {}).get(skill_level, None)
            if not skill_class:
                continue  # 스킬 클래스 없음 → 안 그림

            # 스킬 인스턴스가 아이콘 정보를 제공한다면
            temp_skill = skill_class(self.player)  # 아이콘 정보만 얻기 위해 임시 생성
            if hasattr(temp_skill, "get_icon_clip"):
                draw_rectangle(x - skill_size // 2, y - skill_size // 2,
                               x + skill_size // 2, y + skill_size // 2, 255, 255, 255, 255, True)

                image, (sx, sy, sw, sh) = temp_skill.get_icon_clip()
                image.clip_draw(sx, sy, sw, sh, x, y, skill_size, skill_size)
            else:
                # 없으면 사각형으로 기본 표시
                draw_rectangle(x - skill_size // 2, y - skill_size // 2,
                               x + skill_size // 2, y + skill_size // 2)

            # 쿨타임 남았으면 오버레이 + 숫자 표시
            cd = sm.cooldowns.get(slot, 0.0)
            if cd > 0:
                draw_rectangle(x - skill_size // 2, y - skill_size // 2,
                               x + skill_size // 2, y + skill_size // 2,0,0,0,128,True)
                self.font.draw(x -20, y - 10, f"{cd:.1f}", (255, 0, 0))


    def update(self):
        pass
