import pygame
from pygame import *
from PygameSettings import *

# Player class. Change this to include an image
class Player(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
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
    def update(self, up, down, left, right, platforms, counter, sprites, power_list, score, fruit_list):
        # Start with no change in x-position... see what happened
        if up:
            self.rot = 90
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx, self.rect.centery, self.rot)
            self.y = -MOVE_VEL
        elif down:
            self.rot = 270
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.y = MOVE_VEL
        elif left:
            self.rot = 180
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.x = -MOVE_VEL
        elif right:
            self.rot = 0
            self.chompchomp(counter)
            self.rot_center(self.rect.centerx,self.rect.centery, self.rot)
            self.x = MOVE_VEL

        # even if not moving should still be chomping
        else:
            self.StillChompChomp(counter, self.rot)

        # if pacman goes through the tube that wraps the screen
        if self.rect.right > WIN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIN_WIDTH

        # increment in x direction
        self.rect.left += self.x
        
        # do x-axis collisions
        score = self.collide(self.x, 0, platforms, sprites, power_list, fruit_list, score)

        # increment in y direction
        self.rect.top += self.y

        # assuming we're in the air
        self.onGround = False

        # do y-axis collisions
        score = self.collide(0, self.y, platforms, sprites, power_list, fruit_list, score)
        return score


    #rules for when he collides with walls and barriers
    def collide(self, x, y, platforms, sprites,power_list,fruit_list, score):
        for s in sprites:
            if s not in platforms:
                if s != self.rect and self.rect.collidepoint(s.rect.center) and s in power_list:
                    score += 50
                    print(score)
                    sprites.remove(s)
                    power_list.remove(s)

                elif s != self.rect and self.rect.collidepoint(s.rect.center) and s in fruit_list:
                    score += 100
                    print(score)
                    sprites.remove(s)
                    fruit_list.remove(s)

                elif s != self.rect and self.rect.collidepoint(s.rect.center):
                    sprites.remove(s)
                    score += 10
                    print(score)



        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x > 0:
                    self.rect.right = p.rect.left
                    self.x = 0
                    #print ("collide right")
                if x < 0:
                    self.rect.left = p.rect.right
                    self.x = 0
                    #print ("collide left")
                if y > 0:
                    self.rect.bottom = p.rect.top
                    self.y = 0
                    #print("collide bottom"
                if y < 0:
                    self.rect.top = p.rect.bottom
                    self.y = 0
                    #print("collide top")
        return score

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


class Pellets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH // 3, BLOCK_HEIGHT // 3))
        self.image.convert()
        self.image.fill(PACMAN_PEACH)
        self.rect = Rect(x + BLOCK_WIDTH // 3, y + BLOCK_WIDTH // 3, BLOCK_WIDTH // 3, BLOCK_HEIGHT // 3)

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = 0
        self.y = 0
        self.imageOrig = pygame.image.load('power_pellet.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig, (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.rect = Rect(x + BLOCK_WIDTH // 6, y + BLOCK_WIDTH // 8, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = 0
        self.y = 0
        self.imageOrig = pygame.image.load('Items/ITEM_CHERRY.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig, (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.rect = Rect(x + BLOCK_WIDTH // 4, y + BLOCK_WIDTH // 4, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)

