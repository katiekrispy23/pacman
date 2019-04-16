import pygame
from pygame import *
from PygameSettings import *

# Player class. Change this to include an image
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.hitTop = False
        self.image = Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = Rect(x, y, self.width, self.height)

    def update(self, up, down, left, right,platforms):
        # Start with no change in x-position... see what happened
        if up:
            self.yvel = -JUMP_VEL
        if down:
            self.yvel = JUMP_VEL
        if left:
            self.xvel = -MOVE_VEL
        if right:
            self.xvel = MOVE_VEL
        if self.rect.right > WIN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIN_WIDTH
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    #print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    #print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    #print("collide bottom"
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    #print("collide top")


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(PLATFORM_COLOR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass

