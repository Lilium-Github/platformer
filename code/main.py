import pygame
import random
from player import Player
from constants import *
from functions import *

pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((1000, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

offset = 0

fill = 0

keys = [False, False, False, False, False] 

lvl = 1 

sounds = {"jump_sound" : pygame.mixer.Sound(jump),
    "double_jump_sound" : pygame.mixer.Sound(double_jump)}

music = pygame.mixer.music.load('plats/graphics/music.wav')
pygame.mixer.music.play(-1)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.image = pygame.image.load('plats/graphics/enemy.png')
        self.dir = 0
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def update(self, offset):
        if self.dir == RIGHT:
            self.x += 4
        if self.dir == LEFT:
            self.x -= 4
        if self.dir == DOWN:
            self.y += 4
        if self.dir == UP:
            self.y -= 4
        self.x = self.x + offset
        if random.randrange(1, 60) == 1:
            self.dir = random.randrange(0,4)
        

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randrange(1,3)
        self.adder = 1
    def draw(self):
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.size)
    def update(self, offset):
        self.offset = offset
        self.x = self.x + offset
        if random.randrange(1,10) == 1:
            self.size = self.size + self.adder
            if self.size < 2 or self.size > 3:
                self.adder *= -1
        
player = Player(screen,sounds)

starbag = list()
for i in range(100):
    starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))
    
enemies = list()
for i in range(20):
    val = random.randrange(1, 40) + (40*i)
    enemies.append(Enemy(random.randrange(-1600, 2400), val))    

plats = platsmaker()

while not gameover: #GAME LOOP############################################################
    clock.tick(60) #FPS
    
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
                
            if event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
                
            if event.key == pygame.K_UP:
                keys[UP]=True
                
            if event.key == pygame.K_DOWN:
                keys[DOWN]=True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False

            if event.key == pygame.K_UP:
                keys[UP]=False
                
            if event.key == pygame.K_RIGHT:
                keys[RIGHT]= False
                
            if event.key == pygame.K_DOWN:
                keys[DOWN]= False
          
    #physics section--------------------------------------------------------------------    

    offset = player.update(offset, plats,keys)
    
    for i in range(len(plats)):
        for j in range(len(plats[i])):
            plats[i][j].update(offset)
        
    for i in range(len(starbag)):
        starbag[i].update(offset / 2)
        
    for i in range(len(enemies)):
        enemies[i].update(offset)
        
    if player.ypos < -19:
        player.ypos =+ 750
        lvl += 1
        plats = platsmaker()

        starbag = list()
        for i in range(110 + (lvl * 10)):
            starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))

        enemies = list()
        for i in range(40):
            val = random.randrange(1, 40) + (20*i)
            enemies.append(Enemy(random.randrange(-1600, 2400), val))

    
  
    # RENDER Section--------------------------------------------------------------------------------
            
    screen.fill((fill,fill,fill)) #wipe screen so it doesn't smear
  
    
    for i in range(len(plats)):
        for j in range(len(plats[i])):
            plats[i][j].draw(screen)
        
    for i in range(len(enemies)):
        enemies[i].draw()
    
    for i in range(len(starbag)):
        starbag[i].draw()

    player.draw(keys)
                   
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()