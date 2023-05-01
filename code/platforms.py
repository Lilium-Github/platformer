import pygame
import random
from constants import *

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startY = y
        self.offset = 0
        self.adder = random.choice((-1, -0.5, 0, 0.5, 1))
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 200, 10))
         
    def collide(self, px, py):
        if px + 20>self.x and px<self.x + 200 and py+20 >self.y and py+20 <self.y + 20:
            return self.y - 20 
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