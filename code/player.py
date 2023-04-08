import pygame
from constants import *

class Player:
    def __init__(self, screen, sounds):
        self.xpos = 500 #xpos of player
        self.ypos = 700 #ypos of player
        self.vx = 0 #x velocity of player
        self.vy = 0 #y velocity of player

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