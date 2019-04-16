import pygame, math, sys
from pygame import *
from PygameSettings import *

import Map

h = WIN_WIDTH
v = WIN_HEIGHT


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# intro function
def intro():
    # basicFont = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), FLAGS, DEPTH)
    timer = pygame.time.Clock()
    timer.tick(15)
    intro = True
    # what happens when intro is launched
    # loads picture and scales it to the screen
    imgOrig = pygame.image.load('intro.png')
    img = pygame.transform.scale(imgOrig, (h, v - v // 16))
    smallText = pygame.font.Font('freesansbold.ttf', 16)
    medText = pygame.font.Font('freesansbold.ttf', 24)

    while intro:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            # allow user to exit game from intro screen if desired
            if (event.type == pygame.QUIT) or (keys[pygame.K_ESCAPE]):
                pygame.quit()
                quit()
            # exit intro screen
            if keys[pygame.K_RETURN]:
                return
        # intro screen display
        screen.fill(BLACK)
        # text size for intro screen

        # blits image to screen
        screen.blit(img, (0,0))
        #add other text to screen
        TextSurf, introRect = text_objects("Use the arrow keys to control Pacman", smallText, WHITE)
        introRect.center = (h // 2, v - v // 8)
        screen.blit(TextSurf, introRect)

        TextSurf, introRect = text_objects("Eat all the dots to win!", smallText, WHITE)
        introRect.center = (h // 2, v - v // 8 + v // 32)
        screen.blit(TextSurf, introRect)

        TextSurf, introRect = text_objects("Press \'enter\' to Start", medText, WHITE)
        introRect.center = (h // 2, v - v // 32)
        screen.blit(TextSurf, introRect)
        pygame.display.update()