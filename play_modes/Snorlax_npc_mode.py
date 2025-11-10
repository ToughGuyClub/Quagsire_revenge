from pico2d import *

import game_framework
import game_world


s_img=None
p_img=None
def init():
    global s_img
    global p_img

    if s_img==None:

        s_img=load_image(os.path.join('asset/map/town/Snorlax','Normal.png'))
    if p_img==None:
        p_img=load_image(os.path.join('asset/player/Quagsire','Angry.png'))

    pass

def finish():


    pass

def update():
    handle_events()
    pass

def draw():
    clear_canvas()
    game_world.render()
    game_world.render_npc()
    draw_rectangle(0, 0, 1400, 310, 255, 255, 255, 255, True)
    draw_rectangle(10,10,1390,300,0,0,0,255,True)
    draw_rectangle(1180,300,1400,520,255,255,255,255,True)
    draw_rectangle(0,310,220,520,255,255,255,255,True)
    s_img.draw(1290,410,200,200)
    p_img.draw(110,410,200,200)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
    pass

def pause():
    pass
def resume():
    pass
