import pygame
import time
import random
# from pygame import *
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
        self.startx = x
        self.starty = y
        self.rot = 0
        self.t_end = 0
        self.PowerPac = False

        # TODO: Clean this up by putting all image loads into a "sprite.py" file and importing at top (optional)
        # TODO: Just typical commenting and cleaning if anyone gets bored
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
        self.twohundred = pygame.image.load('Sprites/twoHundred.png').convert_alpha()

        self.powerBlue1 = pygame.image.load('Sprites/POWER_GHOST_BLUE1.png').convert_alpha()
        self.powerBlue1 = pygame.transform.scale(self.powerBlue1, (
            BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.powerBlue2 = pygame.image.load('Sprites/POWER_GHOST_BLUE2.png').convert_alpha()
        self.powerBlue2 = pygame.transform.scale(self.powerBlue2, (
            BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.powerWhite1 = pygame.image.load('Sprites/POWER_GHOST_WHITE1.png').convert_alpha()
        self.powerWhite1 = pygame.transform.scale(self.powerWhite1, (
            BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))


        self.imageOrig = self.transformpic(imgFile)
        self.image = self.transformpic(imgFile)
        self.onehundred = self.transformpic(self.onehundred)
        self.twohundred = self.transformpic(self.twohundred)
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
        self.rect = pygame.Rect(x, y, self.width, self.height)

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

    # function to reset pacman to original position and decrease lives by 1
    # if there is no more lives, it calls to the gameOver() loop to show end screen and score
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

    # in charge of the animation when pacman hits a ghost and he "pops"
    def dieAnimation(self, sprites):
        self.image = self.die0
        for img in [self.die1, self.die2, self.die3, self.die4, self.die5, self.die6, self.die7, self.die8, self.die9,
                    self.die10, self.die11]:
            Functions.screen.fill(BLACK)
            sprites.draw(Functions.screen)
            Functions.screen.blit(img, (self.rect.x, self.rect.y))
            pygame.time.delay(100)
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
        pygame.time.delay(250)

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

        # # assuming we're in the air
        # self.onGround = False

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
                if s != self.rect and self.rect.collidepoint(
                        s.rect.center) and s in ghost_list and self.PowerPac == False:
                    pygame.mixer.Sound.play(dieSound)
                    self.dieAnimation(sprites)
                    self.reset(self.lives, sprites)

                if s != self.rect and self.rect.collidepoint(
                        s.rect.center) and s in ghost_list and self.PowerPac == True:
                    Functions.screen.fill(BLACK)
                    sprites.draw(Functions.screen)
                    Functions.screen.blit(self.twohundred, (self.rect.x, self.rect.y))
                    pygame.display.update()
                    pygame.time.delay(250)
                    self.score += 200
                    s.ghostReset()

                # Collide with Power Pellet
                if s != self.rect and self.rect.collidepoint(s.rect.center) and s in power_list:
                    self.score += 50
                    sprites.remove(s)
                    power_list.remove(s)
                    self.PowerPac = True
                    self.t_end = time.time() + 7.5

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

    # used to help the rotation of pacman based on his direction of movement
    def direction(self):
        # if pacman is moving right
        if self.x == MOVE_VEL and self.y == 0:
            self.rot = 0
            self.rot_center(self.rot)
        # if pacman is moving up
        if self.y == -MOVE_VEL and self.x == 0:
            self.rot = 90
            self.rot_center(self.rot)
        # if pacman is moving left
        if self.x == -MOVE_VEL and self.y == 0:
            self.rot = 180
            self.rot_center(self.rot)
        # if pacman is moving down
        if self.y == MOVE_VEL and self.x == 0:
            self.rot = 270
            self.rot_center(self.rot)


# platform class - used in Map()
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(PLATFORM_COLOR)
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass


# barrier class - used in Map()
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT // 3))
        self.image.convert()
        self.image.fill(PINK)
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass


class Pellets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH // 3, BLOCK_HEIGHT // 3))
        self.image.convert()
        self.image.fill(PACMAN_PEACH)
        self.rect = pygame.Rect(x + BLOCK_WIDTH // 3, y + BLOCK_WIDTH // 3, BLOCK_WIDTH // 3, BLOCK_HEIGHT // 3)


class Power(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = 0
        self.y = 0
        self.imageOrig = pygame.image.load('Sprites/power_pellet.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig,
                                            (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.rect = pygame.Rect(x + BLOCK_WIDTH // 6, y + BLOCK_WIDTH // 8, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6,
                                BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = 0
        self.y = 0
        self.imageOrig = pygame.image.load('Items/ITEM_CHERRY.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOrig,
                                            (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.rect = pygame.Rect(x + BLOCK_WIDTH // 4, y + BLOCK_WIDTH // 4, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6,
                                BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.x = 0
        self.y = 0
        self.startx = x
        self.starty = y
        self.GHOST_VEL = GHOST_VEL
        self.imageOrig = pygame.image.load(sprite).convert_alpha()
        self.imageOrig = pygame.transform.scale(self.imageOrig, (
        BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        self.image = pygame.transform.scale(self.imageOrig,
                                            (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))

        self.inkyup1 = pygame.image.load('Sprites/BLUE_GHOST_UP1.png').convert_alpha()
        self.inkyup2 = pygame.image.load('Sprites/BLUE_GHOST_UP2.png').convert_alpha()
        self.inkydown1 = pygame.image.load('Sprites/BLUE_GHOST_DOWN1.png').convert_alpha()
        self.inkydown2 = pygame.image.load('Sprites/BLUE_GHOST_DOWN2.png').convert_alpha()
        self.inkyleft1 = pygame.image.load('Sprites/BLUE_GHOST_LEFT1.png').convert_alpha()
        self.inkyleft2 = pygame.image.load('Sprites/BLUE_GHOST_LEFT2.png').convert_alpha()
        self.inkyright1 = pygame.image.load('Sprites/BLUE_GHOST_RIGHT1.png').convert_alpha()
        self.inkyright2 = pygame.image.load('Sprites/BLUE_GHOST_RIGHT2.png').convert_alpha()
        self.inkyup1 = self.transformpic(self.inkyup1)
        self.inkyup2 = self.transformpic(self.inkyup2)
        self.inkydown1 = self.transformpic(self.inkydown1)
        self.inkydown2 = self.transformpic(self.inkydown2)
        self.inkyleft1 = self.transformpic(self.inkyleft1)
        self.inkyleft2 = self.transformpic(self.inkyleft2)
        self.inkyright1 = self.transformpic(self.inkyright1)
        self.inkyright2 = self.transformpic(self.inkyright2)
        
        self.blinkyup1 = pygame.image.load('Sprites/RED_GHOST_UP1.png').convert_alpha()
        self.blinkyup2 = pygame.image.load('Sprites/RED_GHOST_UP2.png').convert_alpha()
        self.blinkydown1 = pygame.image.load('Sprites/RED_GHOST_DOWN1.png').convert_alpha()
        self.blinkydown2 = pygame.image.load('Sprites/RED_GHOST_DOWN2.png').convert_alpha()
        self.blinkyleft1 = pygame.image.load('Sprites/RED_GHOST_LEFT1.png').convert_alpha()
        self.blinkyleft2 = pygame.image.load('Sprites/RED_GHOST_LEFT2.png').convert_alpha()
        self.blinkyright1 = pygame.image.load('Sprites/RED_GHOST_RIGHT1.png').convert_alpha()
        self.blinkyright2 = pygame.image.load('Sprites/RED_GHOST_RIGHT2.png').convert_alpha()
        self.blinkyup1 = self.transformpic(self.blinkyup1)
        self.blinkyup2 = self.transformpic(self.blinkyup2)
        self.blinkydown1 = self.transformpic(self.blinkydown1)
        self.blinkydown2 = self.transformpic(self.blinkydown2)
        self.blinkyleft1 = self.transformpic(self.blinkyleft1)
        self.blinkyleft2 = self.transformpic(self.blinkyleft2)
        self.blinkyright1 = self.transformpic(self.blinkyright1)
        self.blinkyright2 = self.transformpic(self.blinkyright2)
        
        self.clydeup1 = pygame.image.load('Sprites/ORANGE_GHOST_UP1.png').convert_alpha()
        self.clydeup2 = pygame.image.load('Sprites/ORANGE_GHOST_UP2.png').convert_alpha()
        self.clydedown1 = pygame.image.load('Sprites/ORANGE_GHOST_DOWN1.png').convert_alpha()
        self.clydedown2 = pygame.image.load('Sprites/ORANGE_GHOST_DOWN2.png').convert_alpha()
        self.clydeleft1 = pygame.image.load('Sprites/ORANGE_GHOST_LEFT1.png').convert_alpha()
        self.clydeleft2 = pygame.image.load('Sprites/ORANGE_GHOST_LEFT2.png').convert_alpha()
        self.clyderight1 = pygame.image.load('Sprites/ORANGE_GHOST_RIGHT1.png').convert_alpha()
        self.clyderight2 = pygame.image.load('Sprites/ORANGE_GHOST_RIGHT2.png').convert_alpha()
        self.clydeup1 = self.transformpic(self.clydeup1)
        self.clydeup2 = self.transformpic(self.clydeup2)
        self.clydedown1 = self.transformpic(self.clydedown1)
        self.clydedown2 = self.transformpic(self.clydedown2)
        self.clydeleft1 = self.transformpic(self.clydeleft1)
        self.clydeleft2 = self.transformpic(self.clydeleft2)
        self.clyderight1 = self.transformpic(self.clyderight1)
        self.clyderight2 = self.transformpic(self.clyderight2)

        self.pinkyup1 = pygame.image.load('Sprites/PINK_GHOST_UP1.png').convert_alpha()
        self.pinkyup2 = pygame.image.load('Sprites/PINK_GHOST_UP2.png').convert_alpha()
        self.pinkydown1 = pygame.image.load('Sprites/PINK_GHOST_DOWN1.png').convert_alpha()
        self.pinkydown2 = pygame.image.load('Sprites/PINK_GHOST_DOWN2.png').convert_alpha()
        self.pinkyleft1 = pygame.image.load('Sprites/PINK_GHOST_LEFT1.png').convert_alpha()
        self.pinkyleft2 = pygame.image.load('Sprites/PINK_GHOST_LEFT2.png').convert_alpha()
        self.pinkyright1 = pygame.image.load('Sprites/PINK_GHOST_RIGHT1.png').convert_alpha()
        self.pinkyright2 = pygame.image.load('Sprites/PINK_GHOST_RIGHT2.png').convert_alpha()
        self.pinkyup1 = self.transformpic(self.pinkyup1)
        self.pinkyup2 = self.transformpic(self.pinkyup2)
        self.pinkydown1 = self.transformpic(self.pinkydown1)
        self.pinkydown2 = self.transformpic(self.pinkydown2)
        self.pinkyleft1 = self.transformpic(self.pinkyleft1)
        self.pinkyleft2 = self.transformpic(self.pinkyleft2)
        self.pinkyright1 = self.transformpic(self.pinkyright1)
        self.pinkyright2 = self.transformpic(self.pinkyright2)

        self.rect = pygame.Rect(x + BLOCK_WIDTH // 4, y + BLOCK_WIDTH // 4, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6,
                                BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6)

    def transformpic(self, image):
        image = pygame.transform.scale(image,
                                       (BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6, BLOCK_WIDTH // 2 + BLOCK_WIDTH // 6))
        return image

    def wiggle(self, counter, image1, image2):
        if counter == 0:
            self.image = image1
        if counter == 7:
            self.image = image2

    def ghostReset(self):
        self.rect.centerx, self.rect.centery = self.startx, self.starty

    def updateblinky(self, barriers, player, counter):
        if self.x == 0 and self.y == 0:
            self.x = self.GHOST_VEL

        self.collide(self.x, 0, barriers, player)
        self.collide(0, self.y, barriers, player)
        # increment in x direction
        self.rect.left += self.x

        # increment in y direction
        self.rect.top += self.y

        if self.x == self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.blinkyright1, self.blinkyright2)

        if self.x == -self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.blinkyleft1, self.blinkyleft2)

        if self.x == 0 and self.y == self.GHOST_VEL:
            self.wiggle(counter, self.blinkydown1, self.blinkydown2)

        if self.x == 0 and self.y == -self.GHOST_VEL:
            self.wiggle(counter, self.blinkyup1, self.blinkyup2)

    def updateclyde(self, barriers, player, counter):
        if self.x == 0 and self.y == 0:
            self.x = self.GHOST_VEL

        self.collide(self.x, 0, barriers, player)
        self.collide(0, self.y, barriers, player)
        # increment in x direction
        self.rect.left += self.x

        # increment in y direction
        self.rect.top += self.y
        
        if self.x == self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.clyderight1, self.clyderight2)

        if self.x == -self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.clydeleft1, self.clydeleft2)

        if self.x == 0 and self.y == self.GHOST_VEL:
            self.wiggle(counter, self.clydedown1, self.clydedown2)

        if self.x == 0 and self.y == -self.GHOST_VEL:
            self.wiggle(counter, self.clydeup1, self.clydeup2)

    def updateinky(self, barriers, player, counter):
        if self.x == 0 and self.y == 0:
            self.x = self.GHOST_VEL

        self.collide(self.x, 0, barriers, player)
        self.collide(0, self.y, barriers, player)
        # increment in x direction
        self.rect.left += self.x

        # increment in y direction
        self.rect.top += self.y

        if self.x == self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.inkyright1, self.inkyright2)

        if self.x == -self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.inkyleft1, self.inkyleft2)

        if self.x == 0 and self.y == self.GHOST_VEL:
            self.wiggle(counter, self.inkydown1, self.inkydown2)

        if self.x == 0 and self.y == -self.GHOST_VEL:
            self.wiggle(counter, self.inkyup1, self.inkyup2)

    def updatepinky(self, barriers, player, counter):
        if self.x == 0 and self.y == 0:
            self.x = self.GHOST_VEL

        self.collide(self.x, 0, barriers, player)
        self.collide(0, self.y, barriers, player)
        # increment in x direction
        self.rect.left += self.x

        # increment in y direction
        self.rect.top += self.y
        if self.x == self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.pinkyright1, self.pinkyright2)

        if self.x == -self.GHOST_VEL and self.y == 0:
            self.wiggle(counter, self.pinkyleft1, self.pinkyleft2)

        if self.x == 0 and self.y == self.GHOST_VEL:
            self.wiggle(counter, self.pinkydown1, self.pinkydown2)

        if self.x == 0 and self.y == -self.GHOST_VEL:
            self.wiggle(counter, self.pinkyup1, self.pinkyup2)
        

    def collide(self, x, y, barriers, player):
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
                if x != 0 or y != 0:
                    self.changeDirection(x, y, barriers, player)

    def changeDirection(self, x, y, barriers, player):
        open = ["L", "R", "U", "D"]
        for p in barriers:
            if p.rect.collidepoint((self.rect.centerx, self.rect.top - 6)):
                open.remove("U")
            if p.rect.collidepoint((self.rect.centerx, self.rect.bottom + 6)):
                open.remove("D")
            if p.rect.collidepoint((self.rect.left - 6, self.rect.centery)):
                open.remove("L")
            if p.rect.collidepoint((self.rect.right + 6, self.rect.centerx)):
                open.remove("R")
        dist = (WIN_WIDTH ** 2 + WIN_HEIGHT ** 2)
        min = ""
        N = BLOCK_WIDTH - 2
        M = BLOCK_HEIGHT - 2
        if ((self.rect.centerx + N - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) < dist:
            dist = ((self.rect.centerx + N - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)
            min = "R"
        if ((self.rect.centerx - N - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) < dist:
            dist = ((self.rect.centerx - N - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)
            min = "L"
        if ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - M - player.rect.centery) ** 2) < dist:
            dist = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - M - player.rect.centery) ** 2)
            min = "U"
        if ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery + M - player.rect.centery) ** 2) < dist:
            dist = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery + M - player.rect.centery) ** 2)
            min = "D"

        if min in open:
            print(open)
            if min == "U":
                self.y = -self.GHOST_VEL
                self.x = 0
            if min == "D":
                self.y = self.GHOST_VEL
                self.x = 0
            if min == "R":
                self.y = 0
                self.x = self.GHOST_VEL
            if min == "L":
                self.y = 0
                self.x = -self.GHOST_VEL
            return
        pick = random.randint(0, len(open) - 1)
        print(open[pick])
        if open[pick] == "U":
            self.y = -self.GHOST_VEL
            self.x = 0
        if open[pick] == "D":
            self.y = self.GHOST_VEL
            self.x = 0
        if open[pick] == "R":
            self.y = 0
            self.x = self.GHOST_VEL
        if open[pick] == "L":
            self.y = 0
            self.x = -self.GHOST_VEL
