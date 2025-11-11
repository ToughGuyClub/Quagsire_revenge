from pico2d import *

class Status:
    def __init__(self,player):
        self.current_selected_skill=[0,0]
        self.player=player
        self.arrowR_image=load_image(os.path.join('asset/player/UI', 'arrow_right.png'))
        self.arrowL_image=load_image(os.path.join('asset/player/UI', 'arrow_left.png'))
    def draw(self):
        #기본 창이 될거임
        draw_rectangle(190, 90, 1210, 710, 47, 248, 240, 255, True)
        draw_rectangle(200,100,1200,700,0,0,0,255,True)
        self.draw_skill_icon()
        pass
    def draw_skill_icon(self):
        if not hasattr(self, 'font'):
            self.font = load_font('asset/screen/intro/introFont.ttf', 30)

        skill_size = 64
        spacing = 30
        start_x = 500
        start_y = 600

        # 안전 검사
        if not hasattr(self.player, 'skill_manager'):
            return
        sm = self.player.skill_manager

        # 4개의 슬롯을 순회
        for slot in range(1, 5):
            x = start_x
            y = start_y - (skill_size + spacing) * (slot - 1)

            # 현재 슬롯의 스킬 가져오기
            skill_level = sm.current_skills[slot - 1] if slot - 1 < len(sm.current_skills) else 0
            if skill_level == 0:
                pass
                #continue  # 슬롯에 스킬 없음 → 안 그림

            skill_class = sm.skills.get(slot, {}).get(skill_level, None)
            if not skill_class:
                pass
                #continue  # 스킬 클래스 없음 → 안 그림

            #선택된 스킬 사각형으로 표시하는거임
            if slot - 1 == self.current_selected_skill[0]:
                draw_rectangle(x - skill_size // 2 - 5, y - skill_size // 2 - 5,
                               x + skill_size // 2 + 5, y + skill_size // 2 + 5, 0, 144, 248, 255, True)


            if skill_class is None:
                # 없으면 사각형으로 기본 표시
                draw_rectangle(x - skill_size // 2, y - skill_size // 2,
                               x + skill_size // 2, y + skill_size // 2,255, 255, 255, 255, True)
                # 좌우에 화살표 그림
                self.arrowL_image.draw(x - skill_size - 10, y)
                self.arrowR_image.draw(x + skill_size + 10, y)
                continue
            # 스킬 인스턴스가 아이콘 정보를 제공한다면
            else:

                temp_skill = skill_class(self.player)  # 아이콘 정보만 얻기 위해 임시 생성
                if hasattr(temp_skill, "get_icon_clip"):
                    draw_rectangle(x - skill_size // 2, y - skill_size // 2,
                                   x + skill_size // 2, y + skill_size // 2, 255, 255, 255, 255, True)

                    image, (sx, sy, sw, sh) = temp_skill.get_icon_clip()
                    image.clip_draw(sx, sy, sw, sh, x, y, skill_size, skill_size)
                    # 좌우에 화살표 그림
                    self.arrowL_image.draw(x - skill_size - 10, y)
                    self.arrowR_image.draw(x + skill_size + 10, y)



        pass
    def update(self):

        pass
