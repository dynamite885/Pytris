import pygame
import random
import numpy as np

width = 780
height = 610
fps = 1000

white = (255, 255, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
mazenta = (255, 0, 255)
orange = (255, 127, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
gray = (127, 127, 127)
lightgray = (180, 180, 180)
black = (0, 0, 0)
cell_Colors = [white, cyan, yellow, mazenta, orange, blue, green, red, gray, black]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pytris")
clock = pygame.time.Clock()
mFont = pygame.font.SysFont("arial", 50, True, False)
sText = mFont.render("Press Enter", True, black)
text_rect = sText.get_rect()
text_rect.centerx = round(width/2)
text_rect.centery = round(height/2)
run = True
GameStart = False
hold = np.zeros((6, 2), int)
class inputs:
    moveLeft = False
    moveRight = False
    softDrop = False

    hardDrop = False
    rotateLeft = False
    rotateRight = False
    hold = False

    DAS_LEFT = False
    DAS_RIGHT = False

    SD_ARR_CNT = 0
    L_DAS_CNT = 0
    L_ARR_CNT = 0
    R_DAS_CNT = 0
    R_ARR_CNT = 0
    SD_ARR_VALUE = 5
    DAS_VALUE = 50
    ARR_VALUE = 0

class field:
    matrix = np.zeros((40, 10), int)
    testMatrix = np.zeros((40, 10), int)
    def __init__(self):
        self.clearCnt = 0
        self.tspin = False
    def clearLines(self):
        for i in range(20):
            if np.all(self.testMatrix[20+i]):
                self.matrix[20+i] = 0
                self.testMatrix[20+i] = 0
                self.matrix[:20+i+1] = np.roll(self.testMatrix[:20+i+1], 1, axis=0)
                self.testMatrix[:20+i+1] = np.roll(self.testMatrix[:20+i+1], 1, axis=0)
                self.clearCnt+=1
                nowMino.drawMino()
class mino:
    I = np.array([[0, 1], [1, 1], [2, 1], [3, 1], [1, 0], [3, 19]])
    O = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [4, 19]])
    T = np.array([[0, 1], [1, 0], [1, 1], [2, 1], [3, 0], [3, 19]])
    L = np.array([[0, 1], [1, 1], [2, 0], [2, 1], [4, 0], [3, 19]])
    J = np.array([[0, 0], [0, 1], [1, 1], [2, 1], [5, 0], [3, 19]])
    S = np.array([[0, 1], [1, 0], [1, 1], [2, 0], [6, 0], [3, 19]])
    Z = np.array([[0, 0], [1, 0], [1, 1], [2, 1], [7, 0], [3, 19]])
    X = np.zeros((6, 2), int)
    minoData = [I, O, T, L, J, S, Z]
    rotMat = np.array([[[1, 0], [0, 1]], [[0, -1], [1, 0]], [[-1, 0], [0, -1]], [[0, 1], [-1, 0]]])
    SRS2 = np.array([[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                     [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                     [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                     [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]])
    SRS3 = np.array([[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 
                     [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]], 
                     [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 
                     [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]]])
    SRS4 = np.array([[[0, 0], [-1, 0], [2, 0], [-1, 0], [2, 0]], 
                     [[0, 0], [1, 0], [1, 0], [1, -1], [1, 2]], 
                     [[0, 0], [2, 0], [-1, 0], [2, 1], [-1, 1]], 
                     [[0, 0], [0, 0], [0, 0], [0, 2], [0, -1]]])
    SRS = np.array([SRS2, SRS3, SRS4])
    nexts = [0, 0, 0, 0, 0]
    def __init__(self, newMino):
        self.data = newMino.copy()
        self.testdata = self.data.copy()
        self.ghost = self.data.copy()
    def __del__(self):
        if self.data[4, 1] != 0:
            for i in range(self.data[4, 1]):
                self.rotateMino(-1)
    def drawMino(self):
        for i in range(4):
            field.matrix[self.data[i, 1]+self.data[5, 1], self.data[i, 0]+self.data[5, 0]] = self.data[4, 0]
    def eraseMino(self):
        for i in range(4):
            field.matrix[self.data[i, 1]+self.data[5, 1], self.data[i, 0]+self.data[5, 0]] = 0
    def isBlockedByMovement(self, toX, toY):
        x, y = toX + self.data[5, 0], toY + self.data[5, 1]
        for i in range(4):
            if not ((self.data[i, 0]+x) in range(10) and (self.data[i, 1]+y) in range(40) and field.testMatrix[self.data[i, 1]+y, self.data[i, 0]+x] == 0):
                return False
        return True
    def moveMino(self, toX, toY):
        self.data[5, 0] += toX
        self.data[5, 1] += toY
    def isSRS(self, d):
        self.eraseMino()
        self.testdata = self.data.copy()
        ad = self.data[4, 1].copy()
        self.rotateMino(d)
        bd = self.data[4, 1].copy()
        for i in range(5):
            if self.isBlockedByMovement(self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, ad, i, 0] - self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, bd, i, 0], 
                                        self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, ad, i, 1] - self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, bd, i, 1]):
                self.moveMino(self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, ad, i, 0] - self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, bd, i, 0],
                              self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, ad, i, 1] - self.SRS[np.max(self.minoData[self.data[4, 0]-1][:4])-1, bd, i, 1])
                self.data[:5] = self.testdata[:5].copy()
                return True
        self.data[:5] = self.testdata[:5].copy()
        self.drawMino()
        return False
    def rotateMino(self, d):
        self.data[4, 1] = (self.data[4, 1] + d + 4) % 4
        for i in range(4):
            self.data[i] = np.dot(self.rotMat[d], [self.data[i, 0] + np.max(self.minoData[self.data[4, 0]-1][:4]) * np.min(self.rotMat[d, 1]), self.data[i, 1] + np.max(self.minoData[self.data[4, 0]-1][:4]) * np.min(self.rotMat[d, 0])])
    def holdMino(self):
        global hold
        self.data[5, 0] = self.minoData[self.data[4, 0]-1][5, 0].copy()
        self.data[5, 1] = self.minoData[self.data[4, 0]-1][5, 1].copy()
        if self.data[4, 1] != 0:
            for i in range(self.data[4, 1]):
                self.rotateMino(-1)
        self.data[4, 1] = 0
        if hold[4, 0] == self.X[4, 0]:
            hold = self.data
            self.data = nowBag.nowQueue.pop(0).copy()
        else:
            hold, self.data = self.data.copy(), hold.copy()
    def drawGhost(self):
        self.testdata = self.data.copy()
        while(self.isBlockedByMovement(0, 1)):
            self.moveMino(0, 1)
        self.ghost = self.data.copy()
        self.data = self.testdata.copy()
    def hardDrop(self):
        self.eraseMino()
        self.data = self.ghost.copy()
        self.drawMino()

class bag:
    def __init__(self):
        self.nowQueue = random.sample(mino.minoData, 7) + random.sample(mino.minoData, 7)
    def generateBag(self):
        if len(self.nowQueue) < 10:
            self.nowQueue += random.sample(mino.minoData, 7)
f = field()
nowBag = bag()
nowMino = mino(nowBag.nowQueue.pop(0))
nowMino.drawMino()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key != pygame.K_RETURN and GameStart == False:
                continue
            else:
                GameStart = True
            if event.key == pygame.K_SPACE:
                nowMino.hardDrop()
                nowMino = mino(nowBag.nowQueue.pop(0))
                nowBag.generateBag()
                field.testMatrix = field.matrix.copy()
                nowMino.drawMino()
                f.clearLines()
                inputs.hardDrop = True
                inputs.hold = False
            if event.key == pygame.K_UP and nowMino.isSRS(1):
                nowMino.rotateMino(1)
                nowMino.drawMino()
            if event.key == pygame.K_z and nowMino.isSRS(-1):
                nowMino.rotateMino(-1)
                nowMino.drawMino()
            if event.key == pygame.K_x and nowMino.isSRS(-2):
                nowMino.rotateMino(-2)
                nowMino.drawMino()
            if event.key == pygame.K_LSHIFT and inputs.hold == False:
                nowMino.eraseMino()
                nowMino.holdMino()
                nowMino.drawMino()
                inputs.hold = True
            if event.key == pygame.K_LEFT and nowMino.isBlockedByMovement(-1, 0):
                nowMino.eraseMino()
                nowMino.moveMino(-1, 0)
                nowMino.drawMino()
                inputs.moveLeft = True
            if event.key == pygame.K_RIGHT and nowMino.isBlockedByMovement(1, 0):
                nowMino.eraseMino()
                nowMino.moveMino(1, 0)
                nowMino.drawMino()
                inputs.moveRight = True
            if event.key == pygame.K_DOWN and nowMino.isBlockedByMovement(0, 1):
                inputs.softDrop = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                inputs.L_DAS_CNT = 0
                inputs.L_ARR_CNT = 0
                inputs.moveLeft = False
            if event.key == pygame.K_RIGHT:
                inputs.R_DAS_CNT = 0
                inputs.R_ARR_CNT = 0
                inputs.moveRight = False
            if event.key == pygame.K_DOWN:
                inputs.SD_ARR_CNT = 0
                inputs.softDrop = False
    if inputs.hardDrop:
        inputs.hardDrop = False
    if inputs.moveLeft:
        if inputs.L_DAS_CNT >= inputs.DAS_VALUE and inputs.moveRight == False:
            if inputs.ARR_VALUE == 0:
                nowMino.eraseMino()
                while nowMino.isBlockedByMovement(-1, 0):
                    nowMino.moveMino(-1, 0)
                nowMino.drawMino()
            elif inputs.L_ARR_CNT % inputs.ARR_VALUE == 0 and nowMino.isBlockedByMovement(-1, 0):
                nowMino.eraseMino()
                nowMino.moveMino(-1, 0)
                nowMino.drawMino()
            inputs.L_ARR_CNT+=1
        inputs.L_DAS_CNT+=1
    if inputs.moveRight:
        if inputs.R_DAS_CNT >= inputs.DAS_VALUE and inputs.moveLeft == False:
            if inputs.ARR_VALUE == 0:
                nowMino.eraseMino()
                while nowMino.isBlockedByMovement(1, 0):
                    nowMino.moveMino(1, 0)
                nowMino.drawMino()
            elif inputs.R_ARR_CNT % inputs.ARR_VALUE == 0 and nowMino.isBlockedByMovement(1, 0):
                nowMino.eraseMino()
                nowMino.moveMino(1, 0)
                nowMino.drawMino()
            inputs.R_ARR_CNT+=1
        inputs.R_DAS_CNT+=1
    if inputs.softDrop:
        if inputs.SD_ARR_CNT % inputs.SD_ARR_VALUE == 0 and nowMino.isBlockedByMovement(0, 1):
            nowMino.eraseMino()
            nowMino.moveMino(0, 1)
            nowMino.drawMino()
        inputs.SD_ARR_CNT+=1
    nowMino.drawGhost()
    screen.fill(white)
    for i in range(4):
        pygame.draw.rect(screen, lightgray, ((nowMino.ghost[i, 0]+nowMino.ghost[5, 0])*30+241, (nowMino.ghost[i, 1]+nowMino.ghost[5, 1]-19)*30+1-20, 28, 28))
        pygame.draw.rect(screen, white, ((nowMino.ghost[i, 0]+nowMino.ghost[5, 0])*30+245, (nowMino.ghost[i, 1]+nowMino.ghost[5, 1]-19)*30+5-20, 20, 20))
    for idx_i, val_i in enumerate(field.matrix):
        for idx_j, val_j in enumerate(val_i):
            if field.matrix[idx_i-21, idx_j] != 0:
                pygame.draw.rect(screen, cell_Colors[field.matrix[idx_i-21, idx_j]], (idx_j*30+241, idx_i*30+1-20, 28, 28))
    for i in range(40):
        for j in range(26):
            if j < 8 or j >= 18:
                pygame.draw.rect(screen, lightgray, (j*30, i*30-600+10, 30, 30), 1)
            else:
                pygame.draw.rect(screen, (230, 230, 230), (j*30, i*30-600+10, 30, 30), 1)
    for i in range(5):
        mino.nexts[i] = nowBag.nowQueue[i]
        for j in range(4):
            pygame.draw.rect(screen, cell_Colors[mino.nexts[i][4, 0]], (570+1+mino.nexts[i][j, 0]*30, 60+1-20+mino.nexts[i][j, 1]*30+i*90, 28, 28))
            pygame.draw.rect(screen, cell_Colors[hold[4, 0]], (60+1+hold[j, 0]*30, 60+1-20+hold[j, 1]*30, 28, 28))
    if not GameStart:
        screen.blit(sText, text_rect)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
