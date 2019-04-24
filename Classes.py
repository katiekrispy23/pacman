import pygame, time
from pygame import *
from PygameSettings import *
import Functions
import Sprites

# Player class. Change this to include an image
class Player(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height, lives, score):
        super().__init__()
        self.score = score
        self.lives = lives
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.rot = 0
        self.onGround = False
        self.hitTop = False
        self.imageOrig = self.transformpic(imgFile)
        self.image = self.transformpic(imgFile)
        self.littlebite = pygame.image.load('Sprites/pacman_orig.png').convert_alpha()
        self.circle = pygame.image.load('Sprites/pacman_circle.png').convert_alpha()
        self.bigbite = pygame.image.load('Sprites/pacman_bigbite.png').convert_alpha()
        self.die0 = pygame.image.load('Sprites/die0.png').convert_alpha()
        self.die1 = pygame.image.load('Sprites/die1.png').convert_alpha()
        self.die2 = pygame.image.load('Sprites/die2.png').convert_alpha()
        self.die3 = pygame.image.load('Sprites/die3.png').convert_alpha()
        self.die4 = pygame.image.load('Sprites/die4.png').convert_alpha()
        self.die5 = pygame.image.load('Sprites/die5.png').convert_alpha()
        self.die6 = pygame.image.load('Sprites/die6.png').convert_alpha()
        self.die7 = pygame.image.load('Sprites/die7.png').convert_alpha()
        self.die8 = pygame.image.load('Sprites/die8.png').convert_alpha()
        self.die9 = pygame.image.load('Sprites/die9.png').convert_alpha()
        self.die10 = pygame.image.load('Sprites/die10.png').convert_alpha()
        self.die11 = pygame.image.load('Sprites/die11.png').convert_alpha()
        self.onehundred = pygame.image.load('Sprites/oneHundred.png').convert_alpha()
        self.onehundred = self.transformpic(self.onehundred)
        self.die1 = self.transformpic(self.die1)
        self.die2 = self.transformpic(self.die2)
        self.die3 = self.transformpic(self.die3)
        self.die4 = self.transformpic(self.die4)
        self.die5 = self.transformpic(self.die5)
        self.die6 = self.transformpic(self.die6)
        self.die7 = self.transformpic(self.die7)
        self.die8 = self.transformpic(self.die8)
        self.die9 = self.transformpic(self.die9)
        self.die10 = self.transformpic(self.die10)
        self.die11 = self.transformpic(self.die11)
        self.pacman_little = self.transformpic(self.littlebite)
        self.pacman_circle = self.transformpic(self.circle)
        self.pacman_big = self.transformpic(self.bigbite)
        self.rect = Rect(x, y, self.width, self.height)

    def transformpic(self, image):
        image = pygame.transform.scale(image, (WIN_WIDTH // 20, WIN_WIDTH // 20))
        return image

    # this function will rotate our pacman based on what direction he is going (that way his mouth is always pointing
    # the right way)
    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.imageOrig, angle)

    # makes chewing animation when pacman is in motion
    def chompchomp(self, counter):

        if counter == 0:
            self.imageOrig = self.pacman_big
        if counter == 5:
            self.imageOrig = self.pacman_little
        if counter == 10:
            self.imageOrig = self.pacman_circle

    def reset(self, lives, sprites):
        self.lives -= 1
        if self.lives == 0:
            Functions.gameOver(sprites, self.score)
        else:
            self.rect.centerx, self.rect.centery = 302, 478
            self.x, self.y = 0, 0
        return lives

    # makes chewing animation when pacman is not moving
    def StillChompChomp(self, counter):
        if counter == 0:
            self.imageOrig = self.pacman_big
            self.rot_center(self.rot)
        if counter == 5:
            self.imageOrig = self.pacman_little
            self.rot_center(self.rot)
        if counter == 10:
            self.imageOrig = self.pacman_circle
            self.rot_center(self.rot)

    def dieAnimation(self, sprites):
        self.image = self.die0
        for img in [self.die1, self.die2, self.die3, self.die4, self.die5, self.die6, self.die7, self.die8, self.die9, self.die10, self.die11]:
            Functions.screen.fill(BLACK)
            sprites.draw(Functions.screen)
            Functions.screen.blit(img, (self.rect.x, self.rect.y))
            time.delay(150)
            pygame.display.update()

    # this function will control the points and animations associated with the fruit
    def eatfruit(self, sprites, fruit_list, s):
        self.score += 100
        sprites.remove(s)
        fruit_list.remove(s)
        Functions.screen.fill(BLACK)
        sprites.draw(Functions.screen)
        Functions.screen.blit(self.onehundred, (self.rect.x, self.rect.y))
        pygame.display.update()
        time.delay(250)

    # updates the location and speed based on keyboard inputs
    def update(self, up, down, left, right, platforms, counter, sprites, power_list, fruit_list, ghost_list, barriers):
        # Start with no change in x-position... see what happened
        if up:
            self.chompchomp(counter)
            self.y = -MOVE_VEL
        if down:
            self.chompchomp(counter)
            self.y = MOVE_VEL
        if left:
            self.chompchomp(counter)
            self.x = -MOVE_VEL
        if right:
            self.chompchomp(counter)
            self.x = MOVE_VEL

        # even if not moving should still be chomping
        else:
            self.StillChompChomp(counter)

        # if pacman goes through the tube that wraps the screen
        if self.rect.right > WIN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIN_WIDTH

        # increment in x direction
        self.rect.left += self.x
        
        # do x-axis collisions
        self.collide(self.x, 0, platforms, sprites, power_list, fruit_list, ghost_list, barriers)

        # increment in y direction
        self.rect.top += self.y

        # assuming we're in the air
        self.onGround = False

        # do y-axis collisions
        self.collide(0, self.y, platforms, sprites, power_list, fruit_list, ghost_list, barriers)
        # return score
        self.direction()

    # rules for when he collides with walls and barriers
    def collide(self, x, y, platforms, sprites, power_list, fruit_list, ghost_list, barriers):
        chompSound = pygame.mixer.Sound("Sounds/pacman_chomp.wav")
        fruitSound = pygame.mixer.Sound("Sounds/pacman_eatfruit.wav")
        dieSound = pygame.mixer.Sound("Sounds/pacman_death.wav")

        for s in sprites:
            if s not in platforms:

                # Collide with Ghost
                if s != self.rect and self.rect.collidepoint(s.rect.center) and s in ghost_list:
                    pygame.mixer.Sound.play(dieSound)
                    self.dieAnimation(sprites)
                    self.reset(self.lives, sprites)

                # Collide with Power Pellet
                if s != self.rect and self.rect.collidepoint(s.rect.center) and s in power_list:
                    self.score += 50
                    sprites.remove(s)
                    power_list.remove(s)

                # collide with fruit
                elif s != self.rect and self.rect.collidepoint(s.rect.center) and s in fruit_list:
                    pygame.mixer.Sound.play(fruitSound)
                    self.eatfruit(sprites, fruit_list, s)

                # collide with regular pellet
                elif s != self.rect and self.rect.collidepoint(s.rect.center):
                    pygame.mixer.Sound.play(chompSound)
                    sprites.remove(s)
                    self.score += 10

        for p in barriers:
            if pygame.sprite.collide_rect(self, p):
                if x > 0:
                    self.rect.right = p.rect.left
                    self.x = 0
                if x < 0:
                    self.rect.left = p.rect.right
                    self.x = 0
                if y > 0:
                    self.rect.bottom = p.rect.top
                    self.y = 0
                if y < 0:
                    self.rect.top = p.rect.bottom
                    self.y = 0

    def direction(self):
        if self.x == MOVE_VEL:
            self.rot = 0
            self.rot_center(self.rot)
        if self.x == -MOVE_VEL:
            self.rot = 180
            self.rot_center(self.rot)
        if self.y == MOVE_VEL:
            self.rot = 270
            self.rot_center(self.rot)
        if self.y == -MOVE_VEL:
            self.rot = 90
            self.rot_center(self.rot)


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


# barrier class - used in Map()
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT // 3))
        self.image.convert()
        self.image.fill(PINK)
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
        self.imageOrig = pygame.image.load('Sprites/power_pellet.png').convert_alpha()
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


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = 0
        self.y = 0
        self.imageOrig = pygame.image.load(sprite).convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig, (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.rect = Rect(x + BLOCK_WIDTH // 4, y + BLOCK_WIDTH // 4, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)
