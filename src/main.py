import pygame
import random
from player import Player
from enemy import Enemy
from constants import *
from functions import *

pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((1000, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

#FONTS
font = pygame.font.Font('freesansbold.ttf', 32)

offset = 0

fill = 100

keys = [False, False, False, False, False] 

lvl = 1 

sounds = {"jump_sound" : pygame.mixer.Sound(jump),
    "double_jump_sound" : pygame.mixer.Sound(double_jump)}

music = pygame.mixer.music.load('plats/graphics/music.wav')
pygame.mixer.music.play(-1)

text = font.render('Level: '+str(lvl), True, (200, 200, 0))

healthbar_pic = pygame.image.load('plats/graphics/healthbar.png')

# class Star:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.size = random.randrange(1,3)
#         self.adder = 1
#     def draw(self):
#         pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.size)
#     def update(self, offset):
#         self.offset = offset
#         self.x = self.x + offset
#         if random.randrange(1,10) == 1:
#             self.size = self.size + self.adder
#             if self.size < 2 or self.size > 3:
#                 self.adder *= -1
        
player = Player(sounds)

# starbag = list()
# for i in range(100):
#     starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))
    
enemies = list()
for i in range(4):
    x = random.randrange(-800, 1000)
    y = random.randrange(100,700)
    enemies.append(Enemy(x,y, LEFT))
    enemies.append(Enemy(x+800,y, RIGHT))

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

    offset = player.update(offset, plats, keys)
    player.hurt(enemies)

    if player.health < 1:
        gameover = True
    
    for i in range(len(plats)):
        for j in range(len(plats[i])):
            plats[i][j].update(offset)
        
    # for i in range(len(starbag)):
    #     starbag[i].update(offset / 2)
        
    for i in range(len(enemies)):
        enemies[i].update(offset)
        
    if player.ypos < -19:
        player.ypos =+ 750
        lvl += 1
        plats = platsmaker()

        # starbag = list()
        # for i in range(110 + (lvl * 10)):
        #     starbag.append(Star(random.randrange(-1600, 2400), random.randrange(0,800)))

        enemies = list()
        for i in range(4 + lvl // 2):
            x = random.randrange(-800, 1000)
            y = random.randrange(100,700)
            enemies.append(Enemy(x,y, LEFT))
            enemies.append(Enemy(x+800,y, RIGHT))

    
  
    # RENDER Section--------------------------------------------------------------------------------
            
    screen.fill((fill,fill,fill)) #wipe screen so it doesn't smear
    
    for i in range(len(plats)):
        for j in range(len(plats[i])):
            plats[i][j].draw(screen)
        
    for i in range(len(enemies)):
        enemies[i].draw(screen)
    
    # for i in range(len(starbag)):
    #     starbag[i].draw()

    player.draw(keys, screen)

    text = font.render("level: "+str(lvl), True, (10, 170, 10))#update score number
    screen.blit(text, (850, 20))

    screen.blit(healthbar_pic, (20,20), (0,40 * (player.health-1),240,40))

    print((player.health-1)*40)
                   
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()