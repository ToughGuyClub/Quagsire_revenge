from pico2d import *
import math
import random

import game_world
from enemy.enemy_state_machine import EnemyStateMachine
import os
import game_framework

class Onix:
    image = None

    def __init__(self):
        if Onix.image is None:
            Onix.image = load_image(os.path.join('asset/enemy', 'onix.png'))
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 1
        self.speed = 100

    def update(self):
        pass

    def draw(self):
        pass