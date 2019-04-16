import pygame, sys
from pygame import *
from PygameSettings import *
from Classes import *

BACKGROUND_IMAGE = 'bg.png'
def map():
    global cameraX, cameraY, WIN_HEIGHT, WIN_WIDTH
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), FLAGS, DEPTH)
    timer = pygame.time.Clock()

    up = False
    down = False
    left = False
    right = False

    sprites = pygame.sprite.Group()
    platforms = []

    x = 0
    y = 0
    # The drawing of the level. P means "platform", M stands for "me" (or "MARIO")
    #  You can add different things here
    level = [
            "PPPPPPPPPPPPPPPPPPP",
            "P       PPP       P",
            "P PP PP PPP PP PP P",
            "P PP PP PPP PP PP P",
            "P                 P",
            "P PP P PPPPP P PP P",
            "P    P   P   P    P",
            "PPPP PPP P PPP PPPP",
            "PPPP P       P PPPP",
            "PPPP P PP PP P PPPP",
            "       P   P       ",
            "PPPP P PPPPP P PPPP",
            "PPPP P   M   P PPPP",
            "PPPP P PPPPP P PPPP",
            "P        P        P",
            "P PP PPP P PPP PP P",
            "P  P           P  P",
            "PP P P PPPPP P P PP",
            "P    P   P   P    P",
            "P PPPPPP P PPPPPP P",
            "P                 P",
            "PPPPPPPPPPPPPPPPPPP",]
    # build the level
    playerFlag = True
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                sprites.add(p)
            if col == "M":
                if playerFlag:
                    # Give the player an initial position (x and y) then width and height
                    player = Player(x,y, PLAYER_WIDTH, PLAYER_HEIGHT)
                    sprites.add(player)
                    # Do not allow another player to be added
                    playerFlag = False
            x += BLOCK_WIDTH
        y += BLOCK_HEIGHT
        x = 0

    if playerFlag:
        print("You didn't include a player!")
        pygame.quit()
    total_level_width = len(level[0])*BLOCK_WIDTH
    total_level_height = len(level)*BLOCK_HEIGHT

    # Thanks to "opengameart.org"
    bgIMG = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
    repeatedImageWidth = int(WIN_WIDTH / 2)
    myImage = pygame.transform.scale(bgIMG, (repeatedImageWidth, WIN_HEIGHT))
    # bg = Surface(myImage,repeatedImageWidth, WIN_HEIGHT)
    # bg.convert()

    while 1:
        timer.tick(30)

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
        for x in range(0,int(total_level_width/repeatedImageWidth)+1):
            screen.blit(myImage,(x*repeatedImageWidth,0))


        # update player, draw everything else
        player.update(up, down, left, right, platforms)
        sprites.draw(screen)

        pygame.display.update()