import pygame
import random
from constants import *

class Enemy:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.height = 18
        self.width= 32
        self.dir = direction

        # animation variables
        self.image = pygame.image.load('plats/graphics/enemy.png')
        self.framesize = 32
        self.frameNum = 0
        self.rowNum = 0
        self.ticker = 0

    def draw(self, screen):
        if self.dir == LEFT:
            self.rowNum = 0
        elif self.dir == RIGHT:
            self.rowNum = 1
        
        self.ticker += 1

        if self.ticker % 5 == 0:
            self.frameNum += 1
            if self.frameNum > 3: self.frameNum = 0
        
        screen.blit(self.image, (self.x, self.y), (self.framesize*self.frameNum, self.rowNum*self.framesize, self.framesize, self.framesize))
        
    def update(self, offset):
        if self.dir == RIGHT:
            self.x += 5
        elif self.dir == LEFT:
            self.x -= 5
        self.x = self.x + offset
        
        if self.x < -1000:
            self.x = 2000
        elif self.x > 2000:
            self.x = -1000

    def collide(self, px, py, psize):
        if px + psize - 16>self.x and px + 16<self.x + self.width and py+psize >self.y and py+psize <self.y + self.height:
            return True
        else:
            return False