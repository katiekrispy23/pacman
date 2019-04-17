import pygame
from pygame import *
from PygameSettings import *

# Player class. Change this to include an image
class Player(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.rot = 0
        self.onGround = False
        self.hitTop = False
        self.imageOrig = pygame.transform.scale(imgFile, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.image = pygame.transform.scale(imgFile, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.littlebite = pygame.image.load('pacman_orig.png').convert_alpha()
        self.circle = pygame.image.load('pacman_circle.png').convert_alpha()
        self.bigbite = pygame.image.load('pacman_bigbite.png').convert_alpha()

        self.pacman_little = pygame.transform.scale(self.littlebite, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.pacman_circle = pygame.transform.scale(self.circle, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.pacman_big = pygame.transform.scale(self.bigbite, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        self.rect = Rect(x, y, self.width, self.height)


    # this function will rotate our pacman based on what direction he is going (that way his mouth is always pointing
    # the right way)
    def rot_center(self, x, y, angle):
        self.image = pygame.transform.rotate(self.imageOrig, angle)

    # makes chewing animation when pacman is in motion
    def chompchomp(self, counter):
        if counter == 0:
            self.imageOrig = self.pacman_big
        if counter == 5:
            self.imageOrig = self.pacman_little
        if counter == 10:
            self.imageOrig = self.pacman_circle

    # makes chewing animation when pacman is not moving
    def StillChompChomp(self, counter, rot):
        if counter == 0:
            self.imageOrig = self.pacman_big
            self.rot_center(self.rect.centerx, self.rect.centery, self.rot)
        if counter == 5:
            self.imageOrig = self.pacman_little
            self.rot_center(self.rect.centerx, self.rect.centery, self.rot)
        if counter == 10:
            self.imageOrig = self.pacman_circle
            self.rot_center(self.rect.centerx, self.rect.centery, self.rot)

    # updates the location and speed based on keyboard inputs
    def update(self, up, down, left, right, platforms, counter):
        # Start with no change in x-position... see what happened
        if up:
            self.rot = 90
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx, self.rect.centery, self.rot)
            self.yvel = -MOVE_VEL
        elif down:
            self.rot = 270
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.yvel = MOVE_VEL
        elif left:
            self.rot = 180
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.xvel = -MOVE_VEL
        elif right:
            self.rot = 0
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.xvel = MOVE_VEL

        # even if not moving should still be chomping
        else:
            self.StillChompChomp(counter, self.rot)

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

    #rules for when he collides with walls and barriers
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


# platform class - used in Map()
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(PLATFORM_COLOR)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass