import pygame, sys
from pygame import *
from PygameSettings import *
from Classes import *
import Functions

pacman_little = pygame.image.load('Sprites/pacman_orig.png').convert_alpha()
pacman_circle = pygame.image.load('Sprites/pacman_circle.png').convert_alpha()
pacman_big = pygame.image.load('Sprites/pacman_bigbite.png').convert_alpha()
BACKGROUND_IMAGE = 'Sprites/bg.png'


def map():

    global WIN_HEIGHT, WIN_WIDTH
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
    ghost_list = []
    platforms = []
    barriers = []

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
            "PPPPCP R     PCPPPP",
            "PPPPCP PPDPP PCPPPP",
            "    C  PBQOP  C    ",
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
            if col == "B":
                ghost = Ghost(x, y, "Sprites/BLUE_GHOST_UP.png")
                ghost_list.append(ghost)
                sprites.add(ghost)
            if col == "Q":
                ghost = Ghost(x, y, "Sprites/PINK_GHOST_DOWN.png")
                ghost_list.append(ghost)
                sprites.add(ghost)
            if col == "O":
                ghost = Ghost(x, y, "Sprites/ORANGE_GHOST_UP.png")
                ghost_list.append(ghost)
                sprites.add(ghost)
            if col == "R":
                blinky = Blinky(x, y, "Sprites/RED_GHOST_LEFT.png")
                ghost_list.append(blinky)
                sprites.add(blinky)
            if col == "Y":
                power = Power(x, y)
                power_list.append(power)
                sprites.add(power)
            if col == "P":
                p = Platform(x, y)
                barriers.append(p)
                platforms.append(p)
                sprites.add(p)
            if col == "C":
                pellets = Pellets(x, y)
                sprites.add(pellets)
            if col == "F":
                fruit = Fruit(x, y)
                fruit_list.append(fruit)
                sprites.add(fruit)
            if col == "D":
                barrier = Barrier(x, y)
                barriers.append(barrier)
                sprites.add(barrier)
            if col == "M":
                if playerFlag:
                    # Give the player an initial position (x and y) then width and height
                    player = Player(pacman_little, x, y, PLAYER_WIDTH, PLAYER_HEIGHT, 3, 0)
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
    total_level_height = len(level)

    # Thanks to "opengameart.org"
    bgIMG = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
    repeatedImageWidth = int(WIN_WIDTH)
    myImage = pygame.transform.scale(bgIMG, (repeatedImageWidth, WIN_HEIGHT))
    introMusic = pygame.mixer.Sound("Sounds/pacman_beginning.wav")
    pygame.mixer.Sound.play(introMusic)
    sprites.draw(screen)
    pygame.display.update()
    pygame.time.delay(4000)

    counter = 0
    while 1:
        counter += 1
        timer.tick(60)
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

        if player.PowerPac == True:

            for g in ghost_list:  # make the ghosts blue
                g.image = player.powerBlue

            if player.t_end < time.time():  # if 8 seconds have passed, flip the flag
                for g in ghost_list:
                    g.image = g.imageOrig
                player.PowerPac = False

            # draw background. This is a repeated background
            for x in range(0, int(total_level_width)):
                screen.blit(myImage, (x*repeatedImageWidth, 0))
            # update player, draw everything else
            counter = counter % 15
            player.update(up, down, left, right, platforms, counter, sprites, power_list, fruit_list, ghost_list, barriers)
            blinky.update(barriers)
            sprites.draw(screen)
            Functions.HUD(player.lives, player.score)
            pygame.display.update()


        else:
            # draw background. This is a repeated background
            for x in range(0, int(total_level_width)):
                screen.blit(myImage, (x * repeatedImageWidth, 0))
            # update player, draw everything else
            counter = counter % 15
            player.update(up, down, left, right, platforms, counter, sprites, power_list, fruit_list, ghost_list, barriers)
            blinky.update(barriers)
            sprites.draw(screen)
            Functions.HUD(player.lives, player.score)
            pygame.display.update()
