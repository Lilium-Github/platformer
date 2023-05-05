import pygame
from constants import *

class Player:
    def __init__(self, screen, sounds):
        self.xpos = 500 #xpos of player
        self.ypos = 700 #ypos of player
        self.vx = 0 #x velocity of player
        self.vy = 0 #y velocity of player
        self.friction = 0.15
        self.accel = 0.08
        self.size = 20

        # jumping variables
        self.isOnGround = False
        self.jumps = 1
        self.airJump = False

        # animation variables
        self.sprite = pygame.image.load('plats/graphics/sheep.png') #load your spritesheet
        self.framesize = 20
        self.RowNum = 0
        self.frameNum = 0
        self.ticker = 0
        self.screen = screen

        # sounds
        self.jump_sound = sounds["jump_sound"]
        self.double_jump_sound = sounds["double_jump_sound"]

        # damage vars
        self.invincible = False
        self.invincibleTimer = 0
        self.health = 3

    def draw(self, keys):
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

        self.screen.blit(self.sprite, (self.xpos, self.ypos), (self.framesize*self.frameNum, self.RowNum*self.framesize, self.framesize, self.framesize))

    def update(self, offset, plats, keys):
        iceVal = self.iceCheck(plats[2])

        if iceVal:
            self.friction = -0.3
        else:
            self.friction = 0.225

        offset = 0

        if keys[LEFT]:
            if self.vx > 0:
                self.vx *= -1.1
            elif self.vx == 0:
                self.vx = -2
            self.vx -= self.accel
        elif keys[RIGHT]:
            if self.vx < 0:
                self.vx *= -1.1
            elif self.vx == 0:
                self.vx = 2
            self.vx += self.accel
        else:
            if self.vx < 0:
                self.vx += self.friction
                if self.vx > -0.001:
                    self.vx = 0
            elif self.vx > 0:
                self.vx -= self.friction
                if self.vx < 0.001:
                    self.vx = 0

        if not iceVal:
            if self.vx > 6:
                self.vx = 6
            elif self.vx < -6:
                self.vx = -6
        
        self.xpos += self.vx

        self.isOnGround = False

        # platform collision
        for i in range(len(plats)):
            for j in range(len(plats[i])):
                if plats[i][j].collide(self.xpos, self.ypos, self.size) != False and keys[DOWN] == False:
                    self.jumps = 1
                    if self.vy > 0:
                        self.vy = 0
                    self.ypos = plats[i][j].collide(self.xpos, self.ypos, self.size)
                    self.isOnGround = True
                    if i == 1:
                        print("bounce")
                        plats[i][j].y += 10
                        self.vy -= 15
                    else: 
                        self.airJump = False
                    
                    self.xpos += plats[i][j].adder *2

        if self.xpos > 700:
            offset = 700 - self.xpos
            self.xpos = 700
        elif self.xpos < 300:
            offset = 300 - self.xpos
            self.xpos = 300

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
                pygame.mixer.Sound.play(self.jump_sound)
            elif self.isOnGround == False and self.airJump:
                self.jumps -= 1
                print("airjump")
                pygame.mixer.Sound.play(self.double_jump_sound)
            
        #gravity
        if self.isOnGround == False:
            self.vy+=.4 #notice this grows over time, aka ACCELERATION
            if keys[UP] == False:
                self.airJump = True
             
        self.ypos+=self.vy

        return offset
    
    def iceCheck(self,icelist):
        for i in range(len(icelist)):
            if icelist[i].collide(self.xpos, self.ypos, self.size):
                return True
        return False
    
    def hurt(self, enemies):
        for index, enemy in enumerate(enemies):
            if enemy.collide(self.xpos, self.ypos, self.size) and not self.invincible:
                print("ow!", self.health)
                self.health -= 1

                del enemy

                self.invincible = True
                self.invincibleTimer = 10

        if self.invincibleTimer > 0:
            self.invincibleTimer -= 1
        else:
            self.invincible = False