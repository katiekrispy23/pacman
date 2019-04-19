import pygame, math, sys
from pygame import *
from PygameSettings import *
import Map

h = WIN_WIDTH
v = WIN_HEIGHT
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS, DEPTH)
timer = pygame.time.Clock()

# used for in game text
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# intro function
def intro():
    timer.tick(15)
    intro = True
    # what happens when intro is launched
    # loads picture and scales it to the screen
    imgOrig = pygame.image.load('Sprites/intro.png')
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
        
        
def HUD(lives, score):
    # draw "lives" on bottom left of screen
    lifeImg =  pygame.image.load('Sprites/life.png')
    lifeImg = pygame.transform.scale(lifeImg, (h // 24, h // 24))

    if lives == 3:
        screen.blit(lifeImg, (h // 18, v - v // 18))
        screen.blit(lifeImg, (2*h // 18, v - v // 18))
        screen.blit(lifeImg, (3*h // 18, v - v // 18))
    if lives == 2:
        screen.blit(lifeImg, (h // 18, v - v // 18))
        screen.blit(lifeImg, (2 * h // 18, v - v // 18))
    if lives == 1:
        screen.blit(lifeImg, (h // 18, v - v // 18))

    # draw "score" on top left of screen
    smallText = pygame.font.Font('freesansbold.ttf', 16)
    TextSurf, gameOverRect = text_objects("Score: " + str(score), smallText, WHITE)
    gameOverRect.center = (h // 16 + h // 32, v // 32)
    screen.blit(TextSurf, gameOverRect)
    
# def gameOver(all_sprites_list, score, lives):
#     timer.tick(15)
#     imgOrig = pygame.image.load('explosion.png')
#     img = pygame.transform.scale(imgOrig, (h, v))
#     lose = True
#     # what happens when you lose
#     while lose:
#         for event in pygame.event.get():
#             keys = pygame.key.get_pressed()
#             # exit lose screen
#             if (event.type == pygame.QUIT) or (keys[pygame.K_ESCAPE]):
#                 pygame.quit()
#                 quit()
#             # replay
#             if keys[pygame.K_r]:
#                 all_sprites_list.empty()
#                 lives = 3
#                 score = 0
#                 intro()
#                 # launch game again
#                 # gameloop(lives, score)
#                 # run "main()"?
# 
#             # if you run out of lives
#         if lives == 0:
#             # lose screen
#             screen.fill(BLACK)
#             # text for lose screen
#             mediumText = pygame.font.Font('freesansbold.ttf', 32)
#             smallText = pygame.font.Font('freesansbold.ttf', 16)
#             # blit image to screen at position 0,0
#             screen.blit(img, (0, 0))
#             # add other text to end screen
#             TextSurf, gameOverRect = text_objects("score: " + str(score), mediumText, WHITE)
#             gameOverRect.center = (h // 2, v // 24)
#             screen.blit(TextSurf, gameOverRect)
# 
#             TextSurf, ExitRect = text_objects("Press \'r\' to Restart, or \'esc\' to Exit", smallText, WHITE)
#             ExitRect.center = (h // 2, v - .5 * v // 16)
#             screen.blit(TextSurf, ExitRect)
#         else:
#             all_sprites_list.empty()
#             # launch game again
#             # gameloop(lives, score)
#             # run "intro()"?
#         pygame.display.update()