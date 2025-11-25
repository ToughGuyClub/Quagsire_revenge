from pico2d import *
import math
import random

import game_world
from enemy.enemy_state_machine import EnemyStateMachine
import os
import game_framework
from enemy.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
class Onix:
    image = None

    def __init__(self):
        self.image_idle = load_image(os.path.join('asset/enemy/Onix','Idle-Anim.png'))
        self.image_walk = load_image(os.path.join('asset/enemy/Onix','Walk-Anim.png'))
        self.image_shoot = load_image(os.path.join('asset/enemy/Onix','Shoot-Anim.png'))
        self.image_attack = load_image(os.path.join('asset/enemy/Onix','Attack-Anim.png'))
        self.image_hurt = load_image(os.path.join('asset/enemy/Onix','Hurt-Anim.png'))
        self.image_hop=load_image(os.path.join('asset/enemy/Onix','Hop-Anim.png'))
        self.x, self.y = 400, 300
        self.frameX = 0.0
        self.frameY = 0
        self.dir = 1
        self.speed = 100
        game_world.add_object(self, 2)
    def update(self):
        pass

    def draw(self):
        self.image_idle.clip_draw(int(self.frameX) * 96, self.frameY * 64, 96, 104, self.x, self.y, 400, 400)
        pass