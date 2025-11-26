from pico2d import *

import game_framework
import game_world



dialogue = []
current_index = 0
display_text = ""          # 현재 화면에 출력되는 문자열
char_index = 0             # 현재 대사에서 몇 글자까지 출력됐는지
text_speed = 0.03          # 한 글자 출력 간격 (초)
text_timer = 0.0           # 타이머
font = None
players_quest_status=None
def init():
    global s_img
    global p_img
    global font,players_quest_status

    if font==None:
        font = load_font('asset/screen/intro/introFont.ttf', 30)
    global dialogue, current_index
    current_index = 0

    from player.character import Character
    for layer in game_world.world_persistent:
        for o in layer:
            if isinstance(o,Character):  # 예시) Character 클래스에 player_flag=True 넣어두면 탐색 가능
                if players_quest_status==None:
                    players_quest_status=o.quest_manager
                    break


    dialogue = ["벌써 여기까지 오다니",
                "너를 잡아가면 지우가 밥셔틀에서 풀어준다고했어!!",
                "널잡아서 이 지긋지긋 노예생활을 끝낼거야",
                "배틀이다 누오!"]
    reset_dialogue_state()
    s_img=load_image(os.path.join('asset/enemy/onix', 'LEADER_Brock.png'))
    p_img=load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
    pass

def finish():


    pass

def update():
    global text_timer, char_index, display_text

    dt = game_framework.frame_time  # 너가 쓰는 delta time

    if char_index < len(dialogue[current_index]):
        text_timer += dt
        if text_timer >= text_speed:
            text_timer = 0
            display_text += dialogue[current_index][char_index]
            char_index += 1
            players_quest_status.change_step(current_index)
            print(current_index)

    handle_events()
    pass

def draw():
    clear_canvas()
    game_world.render()
    draw_rectangle(0, 0, 1400, 310, 255, 255, 255, 255, True)
    draw_rectangle(10,10,1390,300,0,0,0,255,True)
    draw_rectangle(1180,300,1400,520,255,255,255,255,True)
    draw_rectangle(0,310,220,520,255,255,255,255,True)

    font.draw(50, 200, display_text, (255,255,255))
    #퀘스트 캐릭터 아이콘그리는거
    s_img.draw(1290,410,200,200)
    p_img.draw(110,410,200,200)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    global current_index, display_text, char_index
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
        elif event.key in (SDLK_SPACE, SDLK_RETURN):

            # 아직 타이핑 중이면 즉시 전체 출력
            if char_index < len(dialogue[current_index]):
                display_text = dialogue[current_index]
                char_index = len(dialogue[current_index])
            else:
                # 다음 대사로 이동
                current_index += 1

                # 대사 끝
                if current_index >= len(dialogue):

                    #  대화 종료 → 퀘스트 상태 전환
                    q = players_quest_status.quest_list[players_quest_status.current_index]

                    if q.state == "intro":
                        q.update_state("progress")

                    elif q.state == "progress" and q.current >= q.target:
                        q.update_state("complete")

                    elif q.state == "complete":
                        q.state=="Realcomplete"
                        players_quest_status.clear_quest+=1
                        players_quest_status.current_index += 1  # 다음 퀘스트로 이동

                    game_framework.pop_mode()
                    return

                # 초기화
                display_text = ""
                char_index = 0
    pass

def pause():
    pass
def resume():
    pass
def load_dialogue(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]

def reset_dialogue_state():
    global display_text, char_index, text_timer
    display_text = ""
    char_index = 0
    text_timer = 0