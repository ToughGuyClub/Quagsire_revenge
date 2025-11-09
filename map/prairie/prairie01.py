from pico2d import *
from screen.background import Background
from player.character import Character
from player.character import Bubble
import handleEvent
from map.town.Town import Town
from current_map import CurrentMap
from screen.mainScreen import main_screen
import screen.intro
from enemy.Enemy import Enemy
from player.player_UI import Player_UI
import game_world
width, height =  1400, 800





background = Background()

player = Character(200, 300)
def init():


    map = PRAIRIE01()
    player = Character(current_Map,200, 300)
    player_UI = Player_UI(player)
    enemy = Enemy('trainer_BURGLAR.png', 900, 400, 1,player)

    #랜더링에 필요한것
    game_world.add_object(map, 0)
    game_world.add_object(enemy, 2)

    #상호작용에 필요한 것
    game_world.add_collision_pair('player:enemy', player, None)
    game_world.add_collision_pair('player:enemy', None, enemy)
    game_world.add_collision_pair('bubble:enemy', None, enemy)
    game_world.add_collision_pair('cannon:enemy', None, enemy)
def update():
    global current_Map
    game_world.update()

    #버블 리턴하게함
  #  temp_bubble = handle_events(player,world,current_Map)

    #if isinstance(temp_bubble, Bubble):
    #    bubbles.append(temp_bubble)
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass
def pause():
    pass
def resume():
    pass
def handle_events():
    handleEvent.handle_events(player,game_world,current_Map)

class PRAIRIE01:
    def __init__(self):
        self.image = load_image(os.path.join('asset/map/town', 'town_tile.png'))

    def update(self):
        pass

    def draw(self):
        self.image.draw(width // 2, height // 2, width, height)  # 화면 전체에 맞게 그림

