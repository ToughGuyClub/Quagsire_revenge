from pico2d import *
from frameTimer import *

class intro_screen:
    def __init__(self):
        self.step = 0  # 인트로의 현재 단계
        self.timer = 0 # 다음 단계로 넘어가기 위한 시간 계산용
        self.background = load_image(os.path.join('asset/screen/intro','introBackground.png'))
        self.professor = load_image(os.path.join('asset/screen/intro','introOak.png'))
        self.ball = load_image(os.path.join('asset/screen/intro','introBall.png'))
        self.ballOpen = load_image(os.path.join('asset/screen/intro','introBallOpen.png'))
        self.marill = load_image(os.path.join('asset/screen/intro','introMarill.png'))
        self.truck = load_image(os.path.join('asset/screen/intro','introTruck.png'))
        self.quagsire = load_image(os.path.join('asset/screen/intro','introQuag.png'))
        self.blood = load_image(os.path.join('asset/screen/intro','blood.png'))
        self.font = load_font(os.path.join('asset/screen/intro','introFont.ttf'),30)

        # 등장 위치 초기화
        self.prof_x, self.prof_y = 700, 400
        self.ball_x, self.ball_y = 400, 250
        self.marill_size = 64
        self.ball_frame = 0
        self.truck_x = -100
        self.blood_y=-400

        # 텍스트 관련 변수
        self.dialogues = self.load_dialogues(os.path.join('asset/screen/intro','introtext.txt'))
        self.step = 0
        self.text_index = 0
        self.dialogue_index = 0
        self.text_delay = 0.1  # 한 글자 나올 간격 (초 단위)
        self.text_timer = time.time()  # 이전 시간 기록


    def load_dialogues(self, filename):
        dialogues = {}
        current_step = None
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#STEP'):
                    current_step = int(line.replace('#STEP', '').strip())
                    dialogues[current_step] = []
                elif current_step is not None:
                    dialogues[current_step].append(line)
        return dialogues

    def update(self):
            self.timer += get_frame_time()  # 프레임 시간 누적


            #글자 관련 업데이트
            now = time.time()

            if self.step in self.dialogues:
                lines = self.dialogues[self.step]

                if self.dialogue_index < len(lines):
                    line = lines[self.dialogue_index]

                    # 글자 하나씩 출력
                    if self.text_index < len(line):
                        if now - self.text_timer > self.text_delay:
                            self.text_index += 1
                            self.text_timer = now

                    # 문장 다 나왔으면 클릭 대기
                    else:
                        pass

                else:
                    # 모든 대사가 끝났으면 다음 step으로 이동
                    self.step += 1
                    pass
            # 컷 순서별 진행
            if self.step == 0:
                #  오박사 등장
                self.prof_x += 2
                if self.prof_x >= 800:
                    self.step += 1
                    self.timer = 0
            elif self.step==2:
                if self.ball_y>=300:
                    self.ball_y -=5
                    self.ball_frame = (self.ball_frame + 1) % 6  # 몬스터볼 애니메이션 프레임 업데이트
                else:
                    self.ball_y =-100
                    self.step+=1
            elif self.step==3:
                if self.marill_size<90:
                    self.marill_size+=2
                else:
                    self.step+=1
                    self.dialogue_index=0
                    self.text_index=0
            elif self.step==4:
                pass
            elif self.step==5:
                if self.truck_x < self.prof_x:
                    self.truck_x += 15
                else:
                    self.step += 1
                    self.dialogue_index = 0
                    self.text_index = 0
                if self.truck_x > self.prof_x-200:
                    #피효과
                    self.blood_y=self.prof_y
            elif self.step==6:
                #
                pass




    def draw(self):
        clear_canvas()

        self.background.draw(700, 400, 1400, 800)
        self.professor.draw(self.prof_x, self.prof_y, 280, 350)
        if self.step == 0: #오박사 등장
            self.professor.draw(self.prof_x, self.prof_y, 280, 350)
            self.ball_x=self.prof_x-100
            self.ball_y=self.prof_y
        elif self.step == 1: #오박사 대사
            if self.step in self.dialogues:
                lines = self.dialogues[self.step]
                if self.dialogue_index < len(lines):
                    visible = lines[self.dialogue_index][:self.text_index]
                    self.font.draw(100, 150, visible, (255, 255, 255))

        elif self.step == 2:
            #몬스터볼 던지기
            self.ball.clip_draw(self.ball_frame*32, 0, 32, 64, self.ball_x, self.ball_y, 64, 128)
            if self.ball_y<0:
                #몬스터볼 열림
                self.ballOpen.draw(self.ball_x, 200, 64, 128)
        elif self.step == 3:
            #마릴 등장
            self.marill.draw(self.ball_x, 300, 64+self.marill_size, 64+self.marill_size)
        elif self.step == 4:
            self.marill.draw(self.ball_x, 300, 64 + self.marill_size, 64 + self.marill_size)
            if self.step in self.dialogues:
                lines = self.dialogues[self.step]
                if self.dialogue_index < len(lines):
                    visible = lines[self.dialogue_index][:self.text_index]
                    self.font.draw(100, 150, visible, (255, 255, 255))
        elif self.step == 5:
            #트럭 등장

            self.truck.draw(self.truck_x, 400, 600, 400)
            self.blood.draw(self.prof_x+100,self.blood_y, 338, 477)
            self.marill.draw(self.ball_x, 300, 64 + self.marill_size, 64 + self.marill_size)
        elif self.step == 6:
            #누오 등장 예정
            self.truck.draw(self.truck_x, 400, 600, 400)
            self.blood.draw(self.prof_x + 100, self.blood_y, 338, 477)
            self.blood.draw(self.prof_x + 300, self.blood_y+200, 338, 477)
            self.blood.draw(self.prof_x - 200, self.blood_y-100, 338, 477)
            self.marill.draw(self.ball_x, 300, 64 + self.marill_size, 64 + self.marill_size)
            self.quagsire.draw(self.truck_x+200, 300, 300, 300)

            if self.step in self.dialogues:
                lines = self.dialogues[self.step]
                if self.dialogue_index < len(lines):
                    visible = lines[self.dialogue_index][:self.text_index]
                    self.font.draw(100, 150, visible, (255, 255, 255))