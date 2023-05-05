import pygame
import random
from constants import *

class Enemy:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.size = 16
        self.image = pygame.image.load('plats/graphics/enemy.png')
        self.dir = direction

    def __del__(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def update(self, offset):
        if self.dir == RIGHT:
            self.x += 2
        elif self.dir == LEFT:
            self.x += 2
        self.x = self.x + offset
        
        if self.x < -1000:
            self.x = 2000
        elif self.x > 2000:
            self.x = -1000

    def collide(self, px, py, psize):
        if px + psize>self.x and px<self.x + self.size and py+psize >self.y and py+psize <self.y + self.size:
            return True
        else:
            return False