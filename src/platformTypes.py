import pygame
from platforms import Platform

class BasePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (114, 230, 101)
        self.image = pygame.image.load('plats/graphics/platform.png')

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Cloud(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (255, 201, 241)
        self.image = pygame.image.load('plats/graphics/cloud.png')
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Ice(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (153, 208, 232)
        self.image = pygame.image.load('plats/graphics/ice.png')

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))