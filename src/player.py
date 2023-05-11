import pygame
from constants import *

class Player:
    def __init__(self, sounds):
        self.xpos = 500 #xpos of player
        self.ypos = 700 #ypos of player
        self.vx = 0 #x velocity of player
        self.vy = 0 #y velocity of player
        self.friction = 0.15
        self.accel = 0.08
        self.size = 40

        self.direction = RIGHT

        # jumping variables
        self.isOnGround = False
        self.jumps = 1
        self.airJump = False

        # animation variables
        self.sprite = pygame.image.load('plats/graphics/player.png') #load your spritesheet
        self.frameHeight = 40
        self.frameWidth = 35
        self.rowNum = 0
        self.frameNum = 0
        self.ticker = 0

        # sounds
        self.jump_sound = sounds["jump_sound"]
        self.double_jump_sound = sounds["double_jump_sound"]

        # damage vars
        self.invincible = False
        self.invincibleTimer = 0
        self.health = 3

    def draw(self, keys, screen):
        if keys[LEFT]:
            self.rowNum = 3
        elif keys[RIGHT]:
            self.rowNum = 2
        elif self.direction == LEFT:
            self.rowNum = 1
        else:
            self.rowNum = 0
        
        self.ticker += 1

        if self.ticker % 10 == 0:
            self.frameNum += 1
            if self.frameNum > 3: self.frameNum = 0
        
        screen.blit(self.sprite, (self.xpos, self.ypos), (self.frameWidth*self.frameNum, self.rowNum*self.frameHeight, self.frameWidth, self.frameHeight))

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

            self.direction = LEFT
        elif keys[RIGHT]:
            if self.vx < 0:
                self.vx *= -1.1
            elif self.vx == 0:
                self.vx = 2
            self.vx += self.accel

            self.direction = RIGHT
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

        if self.ypos > 760:
            self.jumps = 1
            self.isOnGround = True
            self.vy = 0
            self.ypos = 760
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
        toPop = False

        for i in range(len(enemies)):
            if enemies[i].collide(self.xpos, self.ypos, self.size) and not self.invincible:
                self.health -= 1

                toPop = i

                self.invincible = True
                self.invincibleTimer = 10

        if toPop:
            enemies.pop(toPop)

        if self.invincibleTimer > 0:
            self.invincibleTimer -= 1
        else:
            self.invincible = False