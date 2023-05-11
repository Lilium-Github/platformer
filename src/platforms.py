import pygame
import random
from constants import *

class Platform:
    def __init__(self, x, y):
        # Position Vars
        self.x = x
        self.y = y
        self.startY = y
        self.width = 90
        self.height = 15

        # Movement Vars
        self.offset = 0
        self.adder = random.choice((-1, -0.5, 0, 0.5, 1))
         
    def collide(self, px, py, psize):
        if px + psize-16>self.x and px+16<self.x + self.width and py+psize >self.y and py+psize <self.y + psize:
            return self.y - 40 
        else:
            return False
        
    def update(self, offset):
        self.offset = offset
        if self.x < -900 or self.x > 1700:
            self.adder *= -1
        if random.randrange(1,1199) == 1:
            self.adder *= -1
        self.x = self.x + offset + self.adder
        
        if self.y > self.startY:
            self.y -= 1