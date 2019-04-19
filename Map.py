import pygame, sys
from pygame import *
from PygameSettings import *
from Classes import *
import Functions

pacman_little = pygame.image.load('pacman_orig.png').convert_alpha()
pacman_circle = pygame.image.load('pacman_circle.png').convert_alpha()
pacman_big = pygame.image.load('pacman_bigbite.png').convert_alpha()
BACKGROUND_IMAGE = 'bg.png'
# def map():
    # global cameraX, cameraY, WIN_HEIGHT, WIN_WIDTH
    # pygame.init()
    # screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), FLAGS, DEPTH)
    # timer = pygame.time.Clock()
    #
    # up = False
    # down = False
    # left = False
    # right = False
    #
    # sprites = pygame.sprite.Group()
    # platforms = []
    #
    # x = 0
    # y = 0
    # # The drawing of the level. P means "platform", M stands for "me" (or "MARIO")
    # #  You can add different things here
    # level = [
    #         "PPPPPPPPPPPPPPPPPPP",
    #         "P        P        P",
    #         "P PP PPP P PPP PP P",
    #         "P PP PPP P PPP PP P",
    #         "P                 P",
    #         "P PP P PPPPP P PP P",
    #         "P    P   P   P    P",
    #         "PPPP PPP P PPP PPPP",
    #         "PPPP P       P PPPP",
    #         "PPPP P PP PP P PPPP",
    #         "       P   P       ",
    #         "PPPP P PPPPP P PPPP",
    #         "PPPP P   M   P PPPP",
    #         "PPPP P PPPPP P PPPP",
    #         "P        P        P",
    #         "P PP PPP P PPP PP P",
    #         "P  P           P  P",
    #         "PP P P PPPPP P P PP",
    #         "P    P   P   P    P",
    #         "P PPPPPP P PPPPPP P",
    #         "P                 P",
    #         "PPPPPPPPPPPPPPPPPPP",
    #         "PPPPPPPPPPPPPPPPPPP",]
    # # build the level
    # playerFlag = True
    # for row in level:
    #     for col in row:
    #         if col == "P":
    #             p = Platform(x, y)
    #             platforms.append(p)
    #             sprites.add(p)
    #         if col == "M":
    #             if playerFlag:
    #                 # Give the player an initial position (x and y) then width and height
    #                 player = Player(pacman_little, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    #                 sprites.add(player)
    #                 # Do not allow another player to be added
    #                 playerFlag = False
    #         x += BLOCK_WIDTH
    #     y += BLOCK_HEIGHT
    #     x = 0
    #
    # if playerFlag:
    #     print("You didn't include a player!")
    #     pygame.quit()
    # total_level_width = len(level[0])*BLOCK_WIDTH
    # total_level_height = len(level)*BLOCK_HEIGHT
    #
    # # Thanks to "opengameart.org"
    # bgIMG = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
    # repeatedImageWidth = int(WIN_WIDTH / 2)
    # myImage = pygame.transform.scale(bgIMG, (repeatedImageWidth, WIN_HEIGHT))
    # # bg = Surface(myImage,repeatedImageWidth, WIN_HEIGHT)
    # # bg.convert()
    # counter = 0
    # while 1:
    #     counter += 1
    #     timer.tick(30)
    #     for e in pygame.event.get():
    #
    #         if e.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    #         if e.type == KEYDOWN and e.key == K_UP:
    #             up = True
    #         if e.type == KEYDOWN and e.key == K_DOWN:
    #             down = True
    #         if e.type == KEYDOWN and e.key == K_LEFT:
    #             left = True
    #         if e.type == KEYDOWN and e.key == K_RIGHT:
    #             right = True
    #
    #         if e.type == KEYUP and e.key == K_UP:
    #             up = False
    #         if e.type == KEYUP and e.key == K_DOWN:
    #             down = False
    #         if e.type == KEYUP and e.key == K_RIGHT:
    #             right = False
    #         if e.type == KEYUP and e.key == K_LEFT:
    #             left = False
    #
    #     # draw background. This is a repeated background
    #     for x in range(0, int(total_level_width/repeatedImageWidth)+1):
    #         screen.blit(myImage, (x*repeatedImageWidth, 0))
    #     counter = counter % 15
    #
    #     # update player, draw everything else
    #     player.update(up, down, left, right, platforms, counter)
    #
    #
    #     sprites.draw(screen)
    #     Functions.HUD(3,0)
    #     pygame.display.update()

def map():
    # global WIN_HEIGHT, WIN_WIDTH
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), FLAGS, DEPTH)
    timer = pygame.time.Clock()

    up = False
    down = False
    left = False
    right = False

    sprites = pygame.sprite.Group()
    power_list = []
    fruit_list = []
    platforms = []

    x = 0
    y = 0
    # The drawing of the level. P means "platform", M stands for "me" (or "MARIO")
    #  You can add different things here
    level = [
            "PPPPPPPPPPPPPPPPPPP",
            "PCCCCCCCCPCCCCCCCCP",
            "PCPPCPPPCPCPPPCPPCP",
            "PYPPCPPPCPCPPPCPPYP",
            "PCCCCCCCCCCCCCCCCCP",
            "PCPPCPCPPPPPCPCPPCP",
            "PCCCCPCCCPCCCPCCCCP",
            "PPPPCPPPCPCPPPCPPPP",
            "PPPPCP       PCPPPP",
            "PPPPCP PP PP PCPPPP",
            "    C  P   P  C    ",
            "PPPPCP PPPPP PCPPPP",
            "PPPPCP   F   PCPPPP",
            "PPPPCPCPPPPPCPCPPPP",
            "PCCCCCCCCPCCCCCCCCP",
            "PCPPCPPPCPCPPPCPPCP",
            "PYCPCCCCCMCCCCCPCYP",
            "PPCPCPCPPPPPCPCPCPP",
            "PCCCCPCCCPCCCPCCCCP",
            "PCPPPPPPCPCPPPPPPCP",
            "PCCCCCCCCCCCCCCCCCP",
            "PPPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPPPPPP",]
    # build the level
    playerFlag = True
    for row in level:
        for col in row:
            if col == "Y":
                power = Power(x, y)
                power_list.append(power)
                sprites.add(power)
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                sprites.add(p)
            if col == "C":
                pellets = Pellets(x, y)
                sprites.add(pellets)
            if col == "F":
                fruit = Fruit(x, y)
                fruit_list.append(fruit)
                sprites.add(fruit)
            if col == "M":
                if playerFlag:
                    # Give the player an initial position (x and y) then width and height
                    player = Player(pacman_little, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
                    sprites.add(player)
                    # Do not allow another player to be added
                    playerFlag = False
            x += BLOCK_WIDTH
        y += BLOCK_HEIGHT
        x = 0

    if playerFlag:
        print("You didn't include a player!")
        pygame.quit()
    total_level_width = len(level)
    # total_level_height = len(level)

    # Thanks to "opengameart.org"
    bgIMG = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
    repeatedImageWidth = int(WIN_WIDTH)
    myImage = pygame.transform.scale(bgIMG, (repeatedImageWidth, WIN_HEIGHT))

    score = 0
    lives = 3
    counter = 0
    while 1:
        counter += 1
        timer.tick(90)
        pygame.event.pump()
        for e in pygame.event.get():

            if e.type == QUIT:
                pygame.quit()
                sys.exit()

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background. This is a repeated background
        for x in range(0,int(total_level_width)):
            screen.blit(myImage, (x*repeatedImageWidth, 0))

        # update player, draw everything else
        counter = counter % 15
        score = player.update(up, down, left, right, platforms, counter, sprites, power_list, score, fruit_list)
        sprites.draw(screen)
        Functions.HUD(lives, score)
        pygame.display.update()
