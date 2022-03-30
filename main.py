import pygame, sys
from random import *
from pygame.locals import *
from random import *
from pprint import *
from pygame import mixer

FPS = 60
SPRITESIZE = 12
BOARDSIZE = 25

MAGENTA = (156, 39, 176)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

SPRITES = pygame.image.load('sprites.png')
SPRITES2 = pygame.image.load('sprites2.png')
APPLE = pygame.image.load('apple.png')
BACKGROUND = pygame.image.load('board.png')
HEADER = pygame.image.load('scoreboard.png')
NUMBERS = pygame.image.load('numbers.png')
LIGHTNING = pygame.image.load('lightning.png')
STOP = pygame.image.load('stop.png')
MENU = pygame.image.load('menu.png')

SPRITES.set_colorkey(MAGENTA)
SPRITES2.set_colorkey(MAGENTA)
APPLE.set_colorkey(MAGENTA)
HEADER.set_colorkey(MAGENTA)
NUMBERS.set_colorkey(MAGENTA)
LIGHTNING.set_colorkey(MAGENTA)
STOP.set_colorkey(MAGENTA)

HORIZONTAL = (0, 0, 12, 12)
VERTICAL = (0, 12, 12, 12)
DOWNTORIGHT = (12, 0, 12, 12)
UPTORIGHT = (12, 12, 12, 12)
UPTOLEFT = (24, 0, 12, 12)
DOWNTOLEFT = (24, 12, 12, 12)
RIGHTHEAD = (36, 0, 12, 12)
DOWNHEAD = (36, 12, 12, 12)
UPHEAD = (48, 0, 12, 12)
LEFTHEAD = (48, 12, 12, 12)
UPTAIL = (0, 24, 12, 12)
LEFTTAIL = (12, 24, 12, 12)
DOWNTAIL = (24, 24, 12, 12)
RIGHTTAIL = (36, 24, 12, 12)

ZERO = (0, 0, 24, 24)
ONE = (24, 0, 24, 24)
TWO = (48, 0, 24, 24)
THREE = (72, 0, 24, 24)
FOUR = (96, 0, 24, 24)
FIVE = (120, 0, 24, 24)
SIX = (144, 0, 24, 24)
SEVEN = (168, 0, 24, 24)
EIGHT = (192, 0, 24, 24)
NINE = (216, 0, 24, 24)

def main():
    global FPSCLOCK, DISPLAYSURF, size, snake, twosnakes, gamemodes, movelist, movelist2
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((500, 500), RESIZABLE)
    size = Size(500, 500) # originally 350, 420
    showmenu = True
    menu = Menu(False, False, False)
    while showmenu:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                size.resize(event.w, event.h)
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mousex = mousex / size.getMenuMultiplier()
                mousey = mousey / size.getMenuMultiplier()
                # (64, 165) to (410, 187)
                if 64 < mousex < 410 and 165 < mousey < 187:
                    menu.toggleSnakes()
                # (64, 214) to (418, 259)
                if 64 < mousex < 418 and 214 < mousey < 259:
                    menu.toggleLightning()
                # (64, 286) to (468, 332)
                if 64 < mousex < 468 and 286 < mousey < 332:
                    menu.toggleSpeedup()

                # 159, 375 - 297, 436
                if 159 < mousex < 297 and 375 < mousey < 436:
                    showmenu = False

        DISPLAYSURF.blit(menu.getMenu(), (0,0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    gamemodes = Gamemodes(menu.twosnakes, menu.lightning, menu.speedup, 3, 3) # 2 players, lightning, speed increase mode
    if gamemodes.getsnakemode():
        snake = Snake(2)
    else:
        snake = Snake()
    direction = 'up'
    direction2 = 'up'
    lastmove = 'up'
    lastmove2 = 'up'
    go = False # false until first key is pressed

    movelist = []
    movelist2 = []
    iterator = 3
    iterator2 = 3

    resetstuff = False

    while True:
        checkForQuit()

        if resetstuff:
            direction = 'up'
            direction2 = 'up'
            lastmove = 'up'
            lastmove2 = 'up'
            go = False
            snake.reconstruct()
            gamemodes.resetmovespeeds()
            while movelist.__len__() > 0:
                movelist.pop(0)
            while movelist2.__len__() > 0:
                movelist2.pop(0)

            resetstuff = False

        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                size.resize(event.w, event.h)
            if event.type == MOUSEBUTTONDOWN:
                # if the mouseclick is on the reset button, restart = True
                # (135, 24) to (212, 68)
                mousex, mousey = event.pos
                mousex = mousex * 12 / size.getSpriteSize()
                mousey = mousey * 12 / size.getSpriteSize()
                if 135 <= mousex <= 212 and 24 <= mousey <= 68:
                    resetstuff = True
            if event.type == KEYDOWN:
                if not gamemodes.getsnakemode():
                    if (event.key == K_UP or event.key == K_w) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'down':
                                movelist.append('up')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'down':
                            movelist.append('up')
                            go = True
                    elif (event.key == K_RIGHT or event.key == K_d) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'left':
                                movelist.append('right')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'left':
                            movelist.append('right')
                            go = True
                    elif (event.key == K_LEFT or event.key == K_a) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'right':
                                movelist.append('left')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'right':
                            movelist.append('left')
                            go = True
                    elif (event.key == K_DOWN or event.key == K_s) and movelist.__len__() < 3 and go:
                        if movelist.__len__() == 0:
                            if lastmove != 'up':
                                movelist.append('down')
                        elif movelist[movelist.__len__() - 1] != 'up':
                            movelist.append('down')
                else:
                    if (event.key == K_w) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'down':
                                movelist.append('up')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'down':
                            movelist.append('up')
                            go = True
                    elif (event.key == K_d) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'left':
                                movelist.append('right')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'left':
                            movelist.append('right')
                            go = True
                    elif (event.key == K_a) and movelist.__len__() < 3:
                        if movelist.__len__() == 0:
                            if lastmove != 'right':
                                movelist.append('left')
                                go = True
                        elif movelist[movelist.__len__() - 1] != 'right':
                            movelist.append('left')
                            go = True
                    elif (event.key == K_s) and movelist.__len__() < 3 and go:
                        if movelist.__len__() == 0:
                            if lastmove != 'up':
                                movelist.append('down')
                        elif movelist[movelist.__len__() - 1] != 'up':
                            movelist.append('down')
                    elif (event.key == K_UP) and movelist2.__len__() < 3:
                        if movelist2.__len__() == 0:
                            if lastmove2 != 'down':
                                movelist2.append('up')
                                go = True
                        elif movelist2[movelist2.__len__() - 1] != 'down':
                            movelist2.append('up')
                            go = True
                    elif (event.key == K_RIGHT) and movelist2.__len__() < 3:
                        if movelist2.__len__() == 0:
                            if lastmove2 != 'left':
                                movelist2.append('right')
                                go = True
                        elif movelist2[movelist2.__len__() - 1] != 'left':
                            movelist2.append('right')
                            go = True
                    elif (event.key == K_LEFT) and movelist.__len__() < 3:
                        if movelist2.__len__() == 0:
                            if lastmove2 != 'right':
                                movelist2.append('left')
                                go = True
                        elif movelist2[movelist2.__len__() - 1] != 'right':
                            movelist2.append('left')
                            go = True
                    elif (event.key == K_DOWN) and movelist2.__len__() < 3 and go:
                        if movelist2.__len__() == 0:
                            if lastmove2 != 'up':
                                movelist2.append('down')
                        elif movelist2[movelist2.__len__() - 1] != 'up':
                            movelist2.append('down')

        if iterator >= gamemodes.getmovespeed1():
            if go:
                if movelist.__len__() != 0:
                    direction = movelist[0]
                    resetstuff = snake.move(movelist.pop(0))
                else:
                    resetstuff = snake.move(lastmove)
                if lastmove != direction:
                    snake.turn()
                lastmove = direction
                iterator = 0
        else:
            iterator += 0.5

        if gamemodes.getsnakemode() and go and iterator2 >= gamemodes.getmovespeed2() and not resetstuff:
            if movelist2.__len__() != 0:
                direction2 = movelist2[0]
                resetstuff = snake.move2(movelist2.pop(0))
            else:
                resetstuff = snake.move2(lastmove2)
            if lastmove2 != direction2:
                snake.turn2()
            lastmove2 = direction2
            iterator2 = 0
        else:
            iterator2 += 0.5
        if not resetstuff:
            displayGame()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def getNumberSurface(num):
    num = str(num)
    if len(num) == 1:
        num = '00' + num
    elif len(num) == 2:
        num = '0' + num
    length = len(num) * 24
    surface = pygame.Surface((length, 24))
    characters = list(num)
    for i in range(int(length / 24)):
        sprite = None
        if characters[i] == '0':
            sprite = ZERO
        if characters[i] == '1':
            sprite = ONE
        if characters[i] == '2':
            sprite = TWO
        if characters[i] == '3':
            sprite = THREE
        if characters[i] == '4':
            sprite = FOUR
        if characters[i] == '5':
            sprite = FIVE
        if characters[i] == '6':
            sprite = SIX
        if characters[i] == '7':
            sprite = SEVEN
        if characters[i] == '8':
            sprite = EIGHT
        if characters[i] == '9':
            sprite = NINE
        surface.blit(NUMBERS, (24 * i, 0), sprite)
    surface = pygame.transform.scale(surface, (size.getSpriteSize() * length / 12, size.getSpriteSize() * 2))
    surface.set_colorkey(BLACK)
    return surface

def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back

def lose():
    restart = False
    while not restart:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                size.resize(event.w, event.h)
            if event.type == MOUSEBUTTONDOWN:
                # if the mouseclick is on the reset button, restart = True
                # (135, 24) to (212, 68)
                mousex, mousey = event.pos
                mousex = mousex * 12 / size.getSpriteSize()
                mousey = mousey * 12 / size.getSpriteSize()
                if 135 <= mousex <= 212 and 24 <= mousey <= 68:
                    restart = True
                    # write some code here to restart the game
            if event.type == KEYDOWN:
                if event.key == K_KP_ENTER or event.key == K_RETURN:
                    restart = True
        snake.reconstruct()
        gamemodes.resetmovespeeds()
        while movelist.__len__() > 0:
            movelist.pop(0)
        while movelist2.__len__() > 0:
            movelist2.pop(0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def displayGame():
    boardsize = size.getBoardSize()
    surface = pygame.Surface((boardsize, boardsize))
    DISPLAYSURF.fill(BLACK)
    surface = pygame.transform.scale(BACKGROUND, (boardsize, boardsize))
    DISPLAYSURF.blit(surface, size.getTopLeftBoard())
    surface2 = pygame.transform.scale(HEADER, (size.getBoardSize(), size.getSpriteSize() * 70 / 12))
    surface2.set_colorkey(MAGENTA)
    # start number at 236+25 in x, 35 in y
    DISPLAYSURF.blit(surface2, (size.getSpriteSize() * 25 / 12, 0))
    if gamemodes.getsnakemode():
        scoreSurface = getNumberSurface(snake.length + snake.length2 - 4)
    else:
        scoreSurface = getNumberSurface(snake.length - 2)
    DISPLAYSURF.blit(scoreSurface, (261 * size.getSpriteSize()/12, 35 * size.getSpriteSize()/12))
    for x in range(25):
        for y in range(25):
            if snake.getSegment(x, y).getSprite():
                surface2 = pygame.Surface((12, 12))
                if snake.getSegment(x, y).getSprite() != 'apple' and snake.getSegment(x, y).getSprite() != 'lightning':
                    if snake.getSegment(x, y).getSnake() == 1:
                        surface2.blit(SPRITES, (0, 0), snake.getSegment(x, y).getSprite())
                    elif snake.getSegment(x, y).getSnake() == 2:
                        surface2.blit(SPRITES2, (0, 0), snake.getSegment(x, y).getSprite())

                else:
                    if snake.getSegment(x, y).getSprite() == 'apple':
                        surface2.blit(APPLE, (0,0))
                    else:
                        surface2.blit(LIGHTNING, (0,0))
                surface2 = pygame.transform.scale(surface2, (size.getSpriteSize()+1, size.getSpriteSize()+1))
                surface2.set_colorkey(BLACK)
                DISPLAYSURF.blit(surface2, size.getTopLeftCoords(x, y))

class Segment:
    def __init__(self, lifetime, type, snake = 1):
        self.snake = snake
        self.lifetime = lifetime
        self.type = type
        self.obstacle = False
        if self.type == 'up':
            self.sprite = UPHEAD
            self.obstacle = True
        elif self.type == 'down':
            self.sprite = DOWNHEAD
            self.obstacle = True
        elif self.type == 'right':
            self.sprite = RIGHTHEAD
            self.obstacle = True
        elif self.type == 'left':
            self.sprite = LEFTHEAD
            self.obstacle = True
        elif self.type == 'apple':
            self.sprite = 'apple'
        elif self.type == 'lightning':
            self.sprite = 'lightning'
        elif self.type == None:
            self.sprite = None

    def getSprite(self):
        return self.sprite

    def getSnake(self):
        return self.snake

    def addOneLife(self, snake):
        if self.snake == snake:
            self.lifetime += 1

    def makeUpTail(self):
        self.sprite = UPTAIL

    def makeApple(self):
        self.sprite = 'apple'
        self.type = 'apple'

    def makeLightning(self):
        self.sprite = 'lightning'
        self.type = 'lightning'

    # runs every time the snake moves one square
    def update(self, snake = 1):
        if self.snake == snake:
            if self.lifetime > 0:
                self.lifetime -= 1

            if self.sprite == UPHEAD or self.sprite == DOWNHEAD:
                self.sprite = VERTICAL
            if self.sprite == LEFTHEAD or self.sprite == RIGHTHEAD:
                self.sprite = HORIZONTAL

            if self.lifetime == 1:
                if self.type == 'up':
                    self.sprite = UPTAIL
                if self.type == 'down':
                    self.sprite = DOWNTAIL
                if self.type == 'right':
                    self.sprite = RIGHTTAIL
                if self.type == 'left':
                    self.sprite = LEFTTAIL
            if self.lifetime == 0 and self.type != 'apple' and self.type != 'lightning':
                self.type = None
                self.sprite = None
                self.obstacle = False

    def turn(self, direction):
        if self.type == 'up':
            if self.sprite != UPTAIL:
                if direction == 'right':
                    self.sprite = UPTORIGHT
                    self.type = 'right'
                elif direction == 'left':
                    self.sprite = UPTOLEFT
                    self.type = 'left'
            else:
                if direction == 'right':
                    self.sprite = RIGHTTAIL
                    self.type = 'right'
                elif direction == 'left':
                    self.sprite = LEFTTAIL
                    self.type = 'left'
        elif self.type == 'down':
            if self.sprite != DOWNTAIL:
                if direction == 'right':
                    self.sprite = DOWNTORIGHT
                    self.type = 'right'
                elif direction == 'left':
                    self.sprite = DOWNTOLEFT
                    self.type = 'left'
            else:
                if direction == 'right':
                    self.sprite = RIGHTTAIL
                    self.type = 'right'
                elif direction == 'left':
                    self.sprite = LEFTTAIL
                    self.type = 'left'
        elif self.type == 'left':
            if self.sprite != LEFTTAIL:
                if direction == 'up':
                    self.sprite = DOWNTORIGHT
                    self.type = 'up'
                elif direction == 'down':
                    self.sprite = UPTORIGHT
                    self.type = 'down'
            else:
                if direction == 'up':
                    self.sprite = UPTAIL
                    self.type = 'up'
                elif direction == 'down':
                    self.sprite = DOWNTAIL
                    self.type = 'down'
        elif self.type == 'right':
            if self.sprite != RIGHTTAIL:
                if direction == 'up':
                    self.sprite = DOWNTOLEFT
                    self.type = 'up'
                elif direction == 'down':
                    self.sprite = UPTOLEFT
                    self.type = 'down'
            else:
                if direction == 'up':
                    self.sprite = UPTAIL
                    self.type = 'up'
                elif direction == 'down':
                    self.sprite = DOWNTAIL
                    self.type = 'down'

    def getLifetime(self):
        return self.lifetime

    def getObstacle(self):
        return self.obstacle

    def getType(self):
        return self.type

class Menu:
    def __init__(self, twosnakes, lightning, speedup):
        self.twosnakes = twosnakes
        self.lightning = lightning
        self.speedup = speedup

    def toggleSnakes(self):
        if self.twosnakes:
            self.twosnakes = False
        elif not self.twosnakes:
            self.twosnakes = True

    def toggleLightning(self):
        if self.lightning:
            self.lightning = False
        elif not self.lightning:
            self.lightning = True

    def toggleSpeedup(self):
        if self.speedup:
            self.speedup = False
        elif not self.speedup:
            self.speedup = True

    def getMenu(self):
        surface = pygame.Surface((500, 500))
        surface.blit(MENU, (0,0))

        if self.twosnakes:
            pygame.draw.circle(surface, GREEN, (225, 177), 10)
        else:
            pygame.draw.circle(surface, GREEN, (250, 177), 10)
        if self.lightning:
            pygame.draw.circle(surface, GREEN, (225, 249), 10)
        else:
            pygame.draw.circle(surface, GREEN, (250, 249), 10)
        if self.speedup:
            pygame.draw.circle(surface, GREEN, (225, 322), 10)
        else:
            pygame.draw.circle(surface, GREEN, (250, 322), 10)

        if size.width < size.height:
            surface = pygame.transform.scale(surface, (size.width, size.width))
        else:
            surface = pygame.transform.scale(surface, (size.height, size.height))

        return surface

class Gamemodes:
    def __init__(self, twosnakes, lightning, speedup, movespeed1, movespeed2):
        self.twosnakes = twosnakes
        self.lightning = lightning
        self.speedup = speedup
        self.movespeed1 = movespeed1
        self.movespeed2 = movespeed2

    def resetmovespeeds(self):
        self.movespeed1 = 3
        self.movespeed2 = 3

    def changesnakemode(self, twosnakes):
        self.twosnakes = twosnakes

    def changelightningmode(self, lightning):
        self.lightning = lightning

    def changespeedmode(self, speedup):
        self.speedup = speedup

    def addmovespeed1(self, num = 2):
        self.movespeed1 -= (self.movespeed1 * num / 100)

    def addmovespeed2(self, num = 2):
        self.movespeed2 -= (self.movespeed2 * num / 100)

    def getsnakemode(self):
        return self.twosnakes

    def getlightningmode(self):
        return self.lightning

    def getspeedmode(self):
        return self.speedup

    def getmovespeed1(self):
        return self.movespeed1

    def getmovespeed2(self):
        return self.movespeed2

class Snake:
    def __init__(self, snakenum = 1):
        self.snakenum = snakenum
        self.board = [[Segment(0, None) for _ in range(25)] for g in range(25)]
        if snakenum == 1:
            self.board[12][12] = Segment(2, 'up')
            self.board[12][13] = Segment(1, 'up')
            self.board[12][13].makeUpTail()
            self.head = 12, 12
            self.head2 = None
            self.direction = 'up'
            self.direction2 = None
            self.length = 2
            self.length2 = None
            self.spawnApple()
        elif snakenum == 2:
            self.board[9][12] = Segment(2, 'up')
            self.board[9][13] = Segment(1, 'up')
            self.board[15][12] = Segment(2, 'up', 2)
            self.board[15][13] = Segment(1, 'up', 2)
            self.board[9][13].makeUpTail()
            self.board[15][13].makeUpTail()
            self.head = 9, 12
            self.head2 = 15, 12
            self.direction = 'up'
            self.direction2 = 'up'
            self.length = 2
            self.length2 = 2
            self.spawnApple()
            self.spawnApple()

    def reconstruct(self):
        snakenum = self.snakenum
        self.board = [[Segment(0, None) for _ in range(25)] for g in range(25)]
        if snakenum == 1:
            self.board[12][12] = Segment(2, 'up')
            self.board[12][13] = Segment(1, 'up')
            self.board[12][13].makeUpTail()
            self.head = 12, 12
            self.head2 = None
            self.direction = 'up'
            self.direction2 = None
            self.length = 2
            self.length2 = None
            self.spawnApple()
        elif snakenum == 2:
            self.board[9][12] = Segment(2, 'up')
            self.board[9][13] = Segment(1, 'up')
            self.board[15][12] = Segment(2, 'up', 2)
            self.board[15][13] = Segment(1, 'up', 2)
            self.board[9][13].makeUpTail()
            self.board[15][13].makeUpTail()
            self.head = 9, 12
            self.head2 = 15, 12
            self.direction = 'up'
            self.direction2 = 'up'
            self.length = 2
            self.length2 = 2
            self.spawnApple()
            self.spawnApple()

    def spawnApple(self):
        yourmom = True
        while yourmom:
            x = randint(0, 24)
            y = randint(0, 24)
            if not self.board[x][y].getType():
                self.board[x][y].makeApple()
                yourmom = False

    def spawnLightning(self):
        yourdad = True
        while yourdad:
            x = randint(0, 24)
            y = randint(0, 24)
            if not self.board[x][y].getType():
                self.board[x][y].makeLightning()
                yourdad = False

    def changeDirection(self, direction):
        self.direction = direction

    def changeDirection2(self, direction):
        self.direction2 = direction

    def turn(self):
        x, y = self.head
        if self.direction == 'up':
            y+=1
        elif self.direction == 'down':
            y-=1
        elif self.direction == 'right':
            x-=1
        elif self.direction == 'left':
            x+= 1
        self.board[x][y].turn(self.direction)

    def turn2(self):
        x, y = self.head2
        if self.direction2 == 'up':
            y+=1
        elif self.direction2 == 'down':
            y-=1
        elif self.direction2 == 'right':
            x-=1
        elif self.direction2 == 'left':
            x+= 1
        self.board[x][y].turn(self.direction2)

    def move(self, direction):
        x, y = self.head
        cont = True
        self.changeDirection(direction)
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'right':
            x += 1
        elif direction == 'left':
            x -= 1
        if 0 <= x <= 24 and 0 <= y <= 24:
            if not self.board[x][y].getObstacle():
                self.head = x, y
            else:
                lose()
                cont = False
        else:
            lose()
            cont = False
        if cont:
            for i in range(25):
                for j in range(25):
                    self.board[i][j].update()
            if self.board[x][y].getType() == 'apple':
                if gamemodes.getspeedmode():
                    gamemodes.addmovespeed1()
                for i in range(25):
                    for j in range(25):
                        self.board[i][j].addOneLife(1)
                self.length += 1
                self.spawnApple()
                if randint(1,4) == 2 and gamemodes.getlightningmode():
                    self.spawnLightning()
            if self.board[x][y].getType() == 'lightning':
                gamemodes.addmovespeed1(25)
            self.board[x][y] = Segment(self.length, self.direction)
            return False
        return True

    def move2(self, direction):
        x, y = self.head2
        cont = True
        self.changeDirection2(direction)
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'right':
            x += 1
        elif direction == 'left':
            x -= 1
        if 0 <= x <= 24 and 0 <= y <= 24:
            if not self.board[x][y].getObstacle():
                self.head2 = x, y
            else:
                lose()
                cont = False
        else:
            lose()
            cont = False
        if cont:
            for i in range(25):
                for j in range(25):
                    self.board[i][j].update(2)
            if self.board[x][y].getType() == 'apple':
                if gamemodes.getspeedmode():
                    gamemodes.addmovespeed2()
                for i in range(25):
                    for j in range(25):
                        self.board[i][j].addOneLife(2)
                self.length2 += 1
                self.spawnApple()
                if randint(1, 4) == 2 and gamemodes.getlightningmode():
                    self.spawnLightning()
            if self.board[x][y].getType() == 'lightning':
                gamemodes.addmovespeed2(25)
            self.board[x][y] = Segment(self.length2, self.direction2, 2)
            return False
        return True

    def getSegment(self, x, y):
        return self.board[x][y]

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        if width * 300 / 350 < height * 300 / 420:
            self.spriteSize = (width * 300 / 350) / 25
        else:
            self.spriteSize = (height * 300 / 420) / 25

    def resize(self, width, height):
        self.width = width
        self.height = height
        if width * 300 / 350 < height * 300 / 420:
            self.spriteSize = (width * 300 / 350) / 25
        else:
            self.spriteSize = (height * 300 / 420) / 25

    def getMenuMultiplier(self):
        if self.width < self.height:
            return self.width / 500
        else:
            return self.height / 500

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getSpriteSize(self):
        return int(self.spriteSize)

    def getBoardSize(self):
        return int(self.spriteSize * 25)

    def getTopLeftBoard(self):
        return int(self.spriteSize * 25 / 12), int(self.spriteSize * 95 / 12)

    def getTopLeftCoords(self, x, y):
        return int((self.spriteSize * 25 / 12) + self.spriteSize * x), int((self.spriteSize * 95 / 12) + self.spriteSize * y)

if True:
    main()