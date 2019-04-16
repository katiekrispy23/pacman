import pygame
from pygame import *
from PygameSettings import *

# Player class. Change this to include an image
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.hitTop = False
        self.imageOrig = pygame.image.load('pacman_orig.png').convert_alpha()
        self.imageOrig = pygame.transform.scale(self.imageOrig, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.image = pygame.image.load('pacman_orig.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.rect = Rect(x, y, self.width, self.height)


    # this function will rotate our pacman based on what direction he is going (that way his mouth is always pointing
    # the right way)
    def rot_center(self, x, y, angle):
        self.image = pygame.transform.rotate(self.imageOrig, angle)
        self.rect = self.image.get_rect(center =(x, y))

    def update(self, up, down, left, right, platforms):
        # Start with no change in x-position... see what happened
        if up:
            # self.rot_center(self.rect.centerx, self.rect.centery, 90)
            self.yvel = -MOVE_VEL
        if down:
            # self.rot_center(self.rect.centerx,self.rect.centery, 270)
            self.yvel = MOVE_VEL
        if left:
            # self.rot_center(self.rect.centerx,self.rect.centery, 180)
            self.xvel = -MOVE_VEL
        if right:
            # self.rot_center(self.rect.centerx,self.rect.centery, 0)
            self.xvel = MOVE_VEL

        # if pacman goes through the tube that wraps the screen
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

                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(PLATFORM_COLOR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass