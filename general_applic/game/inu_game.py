"""inu game"""

import random
import sys
import time

import pygame
from pygame.locals import *

# constants
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
BASICFONTSIZE = 20
BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

PIPEIMAGE = pygame.image.load("pipe.png")
MOVERATE = 5
PLAYERIMAGE = pygame.image.load("player.png")

# set up pygame
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("inu")


def terminate():
    """terminate game"""
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    """wait for player to press key"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate()
                return


def drawText(text, font, surface, x, y):
    """draw text"""
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def drawPressKeyMsg():
    """draw press key message"""
    presskeysurf = BASICFONT.render("Press a key to play.", True, TEXTCOLOR)
    presskeyrect = presskeysurf.get_rect()
    presskeyrect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(presskeysurf, presskeyrect)


def showStartScreen():
    """show start screen"""
    titlefont = pygame.font.Font("freesansbold.ttf", 100)
    titlesurf1 = titlefont.render("inu", True, TEXTCOLOR, BACKGROUNDCOLOR)
    titlesurf2 = titlefont.render("inu", True, TEXTCOLOR, BACKGROUNDCOLOR)
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BACKGROUNDCOLOR)
        rotatedsurf1 = pygame.transform.rotate(titlesurf1, degrees1)
        rotatedrect1 = rotatedsurf1.get_rect()
        rotatedrect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedsurf1, rotatedrect1)

        rotatedsurf2 = pygame.transform.rotate(titlesurf2, degrees2)
        rotatedrect2 = rotatedsurf2.get_rect()
        rotatedrect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedsurf2, rotatedrect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def checkForKeyPress():
    """check for key press"""
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyupevents = pygame.event.get(KEYUP)
    if len(keyupevents) == 0:
        return None
    if keyupevents[0].key == K_ESCAPE:
        terminate()
    return keyupevents[0].key


PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
GAPSIZE = 100  # gap between pipes


def getRandomPipe():
    """get random pipe"""
    # y of gap between upper and lower pipe
    gapy = random.randint(0, int(WINDOWHEIGHT * 0.6 - PIPEGAPSIZE))
    pipex = WINDOWWIDTH + 10
    pipe = [
        {"x": pipex, "y": -PIPEGAPSIZE - GAPSIZE + gapy},  # upper pipe
        {"x": pipex, "y": gapy},  # lower pipe
    ]
    return pipe


def showGameOverScreen():
    """show game over screen"""
    gameoversurf = BASICFONT.render("Game Over", True, TEXTCOLOR)
    gameoverrect = gameoversurf.get_rect()
    gameoverrect.midtop = (WINDOWWIDTH / 2, 10)
    DISPLAYSURF.blit(gameoversurf, gameoverrect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    waitForPlayerToPressKey()

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    """draw score"""
    scorestr = "Score: %s" % (score)
    scoresurf = BASICFONT.render(scorestr, True, TEXTCOLOR)
    scorerect = scoresurf.get_rect()
    scorerect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoresurf, scorerect)


def drawPipe(pipes):
    """draw pipe"""
    for pipe in pipes:
        if pipe["y"] < 0:
            pipetop = pygame.transform.flip(PIPEIMAGE, False, True)
            DISPLAYSURF.blit(pipetop, (pipe["x"], pipe["y"] + PIPEGAPSIZE))
        else:
            DISPLAYSURF.blit(PIPEIMAGE, (pipe["x"], pipe["y"]))


def movePipe(pipes):
    """move pipe"""
    for pipe in pipes:
        pipe["x"] -= MOVERATE
    return pipes


def isCollide(playerx, playery, upperpipes, lowerpipes):
    """check collision"""
    if playery > WINDOWHEIGHT - 25 or playery < 0:
        return True
    for pipe in upperpipes:
        pipeheight = PIPEIMAGE.get_height()
        if (
            playery < pipeheight + pipe["y"]
            and abs(playerx - pipe["x"]) < PIPEIMAGE.get_width()
        ):
            return True
    for pipe in lowerpipes:
        if (
            playery + PLAYERIMAGE.get_height() > pipe["y"]
            and abs(playerx - pipe["x"]) < PIPEIMAGE.get_width()
        ):
            return True
    return False


def playerShm(playerShm):
    """player shake"""
    if abs(playerShm["val"]) == 8:
        playerShm["dir"] *= -1

    if playerShm["dir"] == 1:
        playerShm["val"] += 1
    else:
        playerShm["val"] -= 1


def runGame():
    """run game"""
    # player x, y position
    playerx = int(WINDOWWIDTH * 0.2)
    playery = int((WINDOWHEIGHT - PLAYERIMAGE.get_height()) / 2)
    playerShm = {"val": 0, "dir": 1}

    # pipe x, y position
    upperpipes = []
    lowerpipes = []
    pipeheight = PIPEIMAGE.get_height()
    for i in range(2):
        upperpipes.append(getRandomPipe())
        lowerpipes.append(getRandomPipe())

    # score
    score = 0
    pipevelx = -4

    # player velocity, max velocity, downward acceleration, acceleration on flap
    playervelx = -9
    playermaxvelx = 10
    playervely = -9
    playerminvely = -8
    playermaxvely = 10
    playeraccy = 1
    playerflapacc = -9
    playerflapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely = playerflapacc
                    playerflapped = True
                    SOUNDSDICT["wing"].play()

        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes)  # hit test
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + PLAYERIMAGE.get_width() / 2
        for pipe in upperpipes:
            pipeMidPos = pipe["x"] + PIPEIMAGE.get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDSDICT["point"].play()

        # player velocity
        if playervely < playermaxvely and not playerflapped:
            playervely += playeraccy
        if playerflapped:
            playerflapped = False
        playerheight = PLAYERIMAGE.get_height()
        playery = playery + min(playervely, WINDOWHEIGHT - playery - playerheight)

        # move pipes to left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe["x"] += pipevelx
            lowerpipe["x"] += pipevelx


def main():
    """main function"""
    pygame.init()
    global FPSCLOCK, DISPLAYSURF, BASICFONT, IMAGESDICT, SOUNDSDICT
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("inu")
    BASICFONT = pygame.font.Font("freesansbold.ttf", 18)
    IMAGESDICT = {
        "background": pygame.image.load("background.png"),
        "player": pygame.image.load("player.png"),
        "pipe": pygame.image.load("pipe.png"),
    }
    SOUNDSDICT = {
        "die": pygame.mixer.Sound("die.wav"),
        "hit": pygame.mixer.Sound("hit.wav"),
        "point": pygame.mixer.Sound("point.wav"),
        "swoosh": pygame.mixer.Sound("swoosh.wav"),
        "wing": pygame.mixer.Sound("wing.wav"),
    }

    while True:
        runGame()
        showGameOverScreen()


if __name__ == "__main__":
    main()
