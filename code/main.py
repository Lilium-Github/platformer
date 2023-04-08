import pygame
import random
from player import Player
from constants import *

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



class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startY = y
        self.offset = 0
        self.adder = random.choice((-1, -0.5, 0, 0.5, 1))
        
        if random.randrange(1,6) == 1:
            self.bounce = True
            self.color = (206,99,255)
        else:
            self.bounce = False
            self.color = (120, 244, 255)
        
    def draw(self):
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
        
player = Player(screen,sounds)

starbag = list()
for i in range(100):
    starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))
    
enemies = list()
for i in range(20):
    val = random.randrange(1, 40) + (40*i)
    enemies.append(Enemy(random.randrange(-1600, 2400), val))    

plats = list()
for i in range(40):
    val = random.randrange(1, 40) + (20*i)
    plats.append(Platform(random.randrange(-1600, 2400), val))



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
    
    for j in range(len(plats)):
        plats[j].update(offset)
        
    for i in range(len(starbag)):
        starbag[i].update(offset / 2)
        
    for i in range(len(enemies)):
        enemies[i].update(offset)
        
    if player.ypos < -19:
        player.ypos =+ 750
        lvl += 1
        plats = list()
        for i in range(40):
            val = random.randrange(1, 10) + (20*i)
            plats.append(Platform(random.randrange(-1600, 2400), val))
            plats[i].adder = (plats[i].adder * lvl / 4) + plats[i].adder
        starbag = list()
        for i in range(110 + (lvl * 10)):
            starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))
        enemies = list()
        for i in range(40):
            val = random.randrange(1, 40) + (20*i)
            enemies.append(Enemy(random.randrange(-1600, 2400), val))

    
  
    # RENDER Section--------------------------------------------------------------------------------
            
    screen.fill((fill,fill,fill)) #wipe screen so it doesn't smear
  
    
    for i in range(len(starbag)):
        starbag[i].draw()
        
    for i in range(len(enemies)):
        enemies[i].draw()
    
    for i in range(len(plats)):
        plats[i].draw()

    player.draw(keys)
                   
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()