from pico2d import *
import time
import game_framework
from frameTimer import get_frame_time
import play_modes.play_mode
# 전역 변수들
background = None
professor = None
ball = None
ballOpen = None
marill = None
truck = None
quagsire = None
blood = None
font = None
dialogues = {}

# 상태 변수
step = 0
timer = 0
text_index = 0
dialogue_index = 0
text_delay = 0.1
text_timer = 0

# 위치 / 애니메이션
prof_x, prof_y = 700, 400
ball_x, ball_y = 400, 500
marill_size = 64
ball_frame = 0
truck_x = -100
blood_y = -400

def load_dialogues(filename):
    d = {}
    current_step = None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#STEP'):
                current_step = int(line.replace('#STEP', '').strip())
                d[current_step] = []
            elif current_step is not None:
                d[current_step].append(line)
    return d

def init():
    global background, professor, ball, ballOpen, marill, truck, quagsire, blood, font
    global dialogues, step, timer, text_index, dialogue_index, text_timer
    global prof_x, prof_y, ball_x, ball_y, marill_size, ball_frame, truck_x, blood_y

    background = load_image('asset/screen/intro/introBackground.png')
    professor = load_image('asset/screen/intro/introOak.png')
    ball = load_image('asset/screen/intro/introBall.png')
    ballOpen = load_image('asset/screen/intro/introBallOpen.png')
    marill = load_image('asset/screen/intro/introMarill.png')
    truck = load_image('asset/screen/intro/introTruck.png')
    quagsire = load_image('asset/screen/intro/introQuag.png')
    blood = load_image('asset/screen/intro/blood.png')
    font = load_font('asset/screen/intro/introFont.ttf', 30)
    dialogues = load_dialogues('asset/screen/intro/introtext.txt')

    # 초기화
    step = 0
    timer = 0
    text_index = 0
    dialogue_index = 0
    text_timer = time.time()

    prof_x, prof_y = 700, 400
    ball_x, ball_y = 400, 500
    marill_size = 64
    ball_frame = 0
    truck_x = -100
    blood_y = -400

def update():
    global step, timer, text_index, dialogue_index, text_timer
    global prof_x, prof_y, ball_y, ball_frame, marill_size, truck_x, blood_y

    timer += get_frame_time()
    now = time.time()

    # 대사 타이핑 효과
    if step in dialogues:
        lines = dialogues[step]
        if dialogue_index < len(lines):
            line = lines[dialogue_index]
            if text_index < len(line):
                if now - text_timer > 0.1:
                    text_index += 1
                    text_timer = now

    # 연출 진행
    if step == 0:
        prof_x += 2
        if prof_x >= 800:
            step += 1
            timer = 0
    elif step == 2:
        if ball_y >= 300:
            ball_y -= 5
            ball_frame = (ball_frame + 1) % 6
        else:
            ball_y = -100
            step += 1
    elif step == 3:
        if marill_size < 90:
            marill_size += 2
        else:
            step += 1
            dialogue_index = 0
            text_index = 0
    elif step == 5:
        if truck_x < prof_x:
            truck_x += 15
        else:
            step += 1
            dialogue_index = 0
            text_index = 0
        if truck_x > prof_x - 200:
            blood_y = prof_y
    elif step == 7:
        #메인게임화면으로 넘어감
        game_framework.change_mode(play_modes.play_mode)
def draw():
    global ball_x
    clear_canvas()
    background.draw(700, 400, 1400, 800)
    professor.draw(prof_x, prof_y, 280, 350)

    if step == 1 and step in dialogues:
        lines = dialogues[step]
        if dialogue_index < len(lines):
            visible = lines[dialogue_index][:text_index]
            font.draw(100, 150, visible, (255, 255, 255))
        ball_x = prof_x - 150

    elif step == 2:
        ball.clip_draw(ball_frame * 32, 0, 32, 64, ball_x, ball_y, 64, 128)
        if ball_y < 0:
            ballOpen.draw(ball_x, 200, 64, 128)
    elif step == 3:
        marill.draw(ball_x, 300, 64 + marill_size, 64 + marill_size)
    elif step == 4:
        marill.draw(ball_x, 300, 64 + marill_size, 64 + marill_size)
        if step in dialogues:
            lines = dialogues[step]
            if dialogue_index < len(lines):
                visible = lines[dialogue_index][:text_index]
                font.draw(100, 150, visible, (255, 255, 255))
    elif step == 5:
        truck.draw(truck_x, 400, 600, 400)
        blood.draw(prof_x + 100, blood_y, 338, 477)
        marill.draw(ball_x, 300, 64 + marill_size, 64 + marill_size)
    elif step == 6:
        truck.draw(truck_x, 400, 600, 400)
        blood.draw(prof_x + 100, blood_y, 338, 477)
        blood.draw(prof_x + 300, blood_y + 200, 338, 477)
        blood.draw(prof_x - 200, blood_y - 100, 338, 477)
        marill.draw(ball_x, 300, 64 + marill_size, 64 + marill_size)
        quagsire.draw(truck_x + 200, 300, 300, 300)

        if step in dialogues:
            lines = dialogues[step]
            if dialogue_index < len(lines):
                visible = lines[dialogue_index][:text_index]
                font.draw(100, 150, visible, (255, 255, 255))

    update_canvas()

def handle_events():
    global step, dialogue_index, text_index

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # 클릭 시 다음 대사로 이동
            if step in dialogues:
                lines = dialogues[step]
                if dialogue_index < len(lines) - 1:
                    dialogue_index += 1
                    text_index = 0
                else:
                    step += 1
                    dialogue_index = 0
                    text_index = 0


def finish():
    global background, professor, ball, ballOpen, marill, truck, quagsire, blood, font
    del background, professor, ball, ballOpen, marill, truck, quagsire, blood, font

def pause(): pass
def resume(): pass
