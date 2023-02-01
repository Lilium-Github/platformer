import pygame
import random
pygame.init()  
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((1000, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop

#CONSTANTS
LEFT=0
RIGHT=1
UP = 2
DOWN = 3
NONE = 4

fill = 0

#player variables
#xpos = 500 #xpos of player
#ypos = 700 #ypos of player
#vx = 0 #x velocity of player
#vy = 0 #y velocity of player
keys = [False, False, False, False, False] #this list holds whether each key has been pressed
#isOnGround = False #this variable stops gravity from pulling you down more when on a platform
offset = 0
#jumps = 1
#airJump = False
lvl = 1

#variables for animation
# frameWidth = 20
# frameHeight = 20
# RowNum = 0 #for left animation, this will need to change for other animations
# frameNum = 0
# ticker = 0

class Player:
    def __init__(self):
        self.xpos = 500 #xpos of player
        self.ypos = 700 #ypos of player
        self.vx = 0 #x velocity of player
        self.vy = 0 #y velocity of player

        # jumping variables
        self.isOnGround = False
        self.jumps = 1
        self.airJump = False

        # animation variables
        self.sprite = pygame.image.load('plats/sheep.png') #load your spritesheet
        self.framesize = 20
        self.RowNum = 0
        self.frameNum = 0
        self.ticker = 0

    def draw(self):
        # ANIMATION
        if keys[RIGHT]==True:
            self.RowNum = 0
            # Ticker is a spedometer. We don't want Link animating as fast as the
            # processor can process! Update Animation Frame each time ticker goes over
            self.ticker+=1
            if self.ticker%10==0: #only change frames every 10 ticks
                self.frameNum+=1
                #If we are over the number of frames in our sprite, reset to 0.
                #In this particular case, there are 4 frames (0 through 3)
            if self.frameNum>3: 
                self.frameNum = 0
        elif keys[LEFT]==True: #left animation
            self.RowNum = 1
            self.ticker+=1
            if self.ticker%10==0:
                self.frameNum+=1
            if self.frameNum>3: 
                self.frameNum = 0

        screen.blit(self.sprite, (self.xpos, self.ypos), (self.framesize*self.frameNum, self.RowNum*self.framesize, self.framesize, self.framesize))

    def update(self, offset, plats):
        # left movement
        if keys[LEFT]==True:
            if self.xpos > 300:
                self.vx = -5
                offset = 0
            else:
                self.xpos = 300
                offset = 5
                self.vx = 0
            self.direction = LEFT
            
        # right movement
        elif keys[RIGHT]==True:
            if self.xpos < 700:
                self.vx = 5
                offset = 0
            else:
                self.xpos = 700
                self.vx = 0
                offset = -5
            self.direction = RIGHT

        # turn off velocity
        else:
            self.vx = 0
            offset = 0

        self.isOnGround = False

        # platform collision
        for i in range(len(plats)):
             if plats[i].collide(self.xpos, self.ypos) != False and keys[DOWN] == False:
                self.jumps = 1
                if self.vy > 0:
                    self.vy = 0
                self.ypos = plats[i].collide(self.xpos, self.ypos)
                self.isOnGround = True
                if plats[i].bounce:
                    plats[i].y += 10
                    self.vy -= 15
                else: 
                    self.airJump = False
                
                if self.xpos > 300 and self.xpos < 700:
                    self.xpos += plats[i].adder * 2
                else:
                    offset -= plats[i].adder * 2


        if self.ypos > 780:
            self.jumps = 1
            self.isOnGround = True
            self.vy = 0
            self.ypos = 780
            self.airJump = False

        #JUMPING
        if keys[UP] and self.jumps > 0 and self.airJump or keys[UP] and self.isOnGround: #only jump when on the ground
            self.vy = -8.8
            self.direction = UP
            if self.isOnGround == True and self.airJump == False:
                self.isOnGround = False
                print("groundjump")
                self.airJump = False
                pygame.mixer.Sound.play(jump_sound)
            elif self.isOnGround == False and self.airJump:
                self.jumps -= 1
                print("airjump")
                pygame.mixer.Sound.play(double_jump_sound)
            
        #gravity
        if self.isOnGround == False:
            self.vy+=.4 #notice this grows over time, aka ACCELERATION
            if keys[UP] == False:
                self.airJump = True
        if offset < 0:
            offset+=.2
        elif offset > 0:
            offset-=.2
        if self.vx < 0:
            self.vx +=.2
        elif self.vx > 0:
            self.vx -= .2
        
        

        #update player position
        self.xpos+=self.vx 
        self.ypos+=self.vy
        
        return offset

        

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.image = pygame.image.load('plats/enemy.png')
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
        
player = Player()

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

jump_sound = pygame.mixer.Sound('plats/jump.wav')
double_jump_sound = pygame.mixer.Sound('plats/double_jump.wav')
music = pygame.mixer.music.load('plats/music.wav')
pygame.mixer.music.play(-1)

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

    offset = player.update(offset, plats)
    
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

    player.draw()
                   
    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------
pygame.quit()