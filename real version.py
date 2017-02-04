import pygame, sys
from random import randint
from pygame.locals import *
import math
import time
import numpy as np

pygame.init()
DISPLAY=pygame.display.set_mode((1000,600),0,32)

white = (255,255,255)

DISPLAY.fill(white)

boxWidth = 100
boxHeight = 36

floors = 3
while (600/3)/boxHeight < floors:
    print "Too Much Floors."
    floors = int(raw_input())

score = 0                       #Blocks broken
x = 0
y = 0

blockArray = []      #For checking if the ball hit any of the blocks

for sum in range((1000/boxWidth) * floors):
    color = (randint(0,255), randint(0,255), randint(0,255))
    pygame.draw.rect(DISPLAY,color,(x,y,boxWidth,boxHeight))
    blockArray.append((x, y))
    x += boxWidth
    if x == 1000:
        y += boxHeight
        x = 0

#define the board
color = (randint(0,255), randint(0,255), randint(0,255))
boardWidth = 100

boardHeight = 10
boardX = 500

#define the ball
color2 = (0,0,0)
ballRadius = 10
ballX = 1000/2 + boardWidth/2
ballY = 600 - boardHeight - ballRadius -1 #-1 is for malfunction of elif in ballFunction

initDir = randint(10, 170)       #Initial direction of the ball
direction = initDir

def ballFunction(d):
    global ballX
    global ballY
    global boardX
    global ballRadius
    global boxWidth
    global direction
    global blockArray
    global score
    pygame.draw.circle(DISPLAY, white, (ballX, ballY), ballRadius)
    if (ballY + ballRadius >= 600 - boardHeight and ballY + ballRadius <= 600) and (ballX + ballRadius >= boardX - 2 and ballX - ballRadius <= boardX + boardWidth + 2): #When the ball hits the board
        if ballX >= boardX - 3 and ballX < boardX + boardWidth/2:
            d = 135
        elif ballX >= boardX + boardWidth/2 and ballX <= boardX + boardWidth + 3:
            d = 45
    elif (ballX - ballRadius <= 0 or ballX + ballRadius >= 1000): #When the ball hits the side walls
        if d >= 0 and d <= 180:
            d = 180 - d
        elif d >= 180 and d <= 360:
            d = 540 - d
    elif (ballY - ballRadius <= 0): #When the ball hits the ceiling
        d = 360 - d
    else:
        for (x, y) in blockArray:     #Check if the ball has hit a block.
            if ballY - ballRadius <= y + boxHeight and ballY - ballRadius >= y:
                if ballX > x and ballX < x + boxWidth:      #When the ball hits the upside or downside of a box.
                    blockArray.remove((x, y))
                    score += 1
                    d = 360 - d
            elif ballY > y and ballY < y + boxHeight:
                if ballX - ballRadius >= x + boxWidth/2 and ballX - ballRadius <= x + boxWidth:      #When the ball hits the right side of a box.
                    if d >= 0 and d <= 180:
                        blockArray.remove((x, y))
                        score += 1
                        d = 180 - d
                    elif d >= 180 and d <= 360:
                        blockArray.remove((x, y))
                        score += 1
                        d = 540 - d
                elif ballX + ballRadius >= x and ballX + ballRadius <= x + boxWidth/2:      #When the ball hits the left side of a box.
                    if d >= 0 and d <= 180:
                        blockArray.remove((x, y))
                        score += 1
                        d = 180 - d
                    elif d >= 180 and d <= 360:
                        blockArray.remove((x, y))
                        score += 1
                        d = 540 - d
    ballX += int(round(np.cos(np.deg2rad(d)) * 10))
    ballY -= int(round(np.sin(np.deg2rad(d)) * 10))
    direction = d                                               
    time.sleep(0.01)                                   
    pygame.draw.circle(DISPLAY, color2, (ballX, ballY), ballRadius)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.draw.rect(DISPLAY,white,(boardX,600 - boardHeight,boardWidth,boardHeight))
    for (x,y) in blockArray:                                    #Erase the boxes every time
        pygame.draw.rect(DISPLAY,(255,255,255),(x,y,boxWidth,boxHeight))
    ballFunction(direction)
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        boardX -= 14
        if boardX < 0:
            boardX = 0
    if keys[K_RIGHT]:   
        boardX += 14
        if boardX > 1000 - boardWidth:
            boardX = 1000 - boardWidth
    pygame.draw.rect(DISPLAY,(randint(0,255), randint(0,255), randint(0,255)),(boardX,600 - boardHeight,boardWidth,boardHeight))
    for (x,y) in blockArray:                                    #Redraw the boxes every time
        ranColor = (randint(0,255), randint(0,255), randint(0,255))
        pygame.draw.rect(DISPLAY,ranColor,(x,y,boxWidth,boxHeight))
    if ballY - ballRadius >= 600:
        DISPLAY.fill((0, 0, 0))
        font = pygame.font.SysFont("monospace", 50)
        label = font.render("Game Over", 1, (255,255,255))
        label2 = font.render("Score = ", 1, (255,255,255))
        label3 = font.render(str(score), 1, (255,255,255))
        DISPLAY.blit(label, (370, 250))
        DISPLAY.blit(label2, (370, 300))
        DISPLAY.blit(label3, (620, 300))
        pygame.display.update()
        time.sleep(5)
        pygame.display.quit()
        sys.exit()
    if  blockArray == []:
        DISPLAY.fill((255, 255, 255))
        font = pygame.font.SysFont("Ariel", 50)
        label = font.render("Game Clear!", 1, (255, 0, 255))
        DISPLAY.blit(label, (370, 250))
        pygame.display.update()
        time.sleep(5)
        pygame.display.quit()
        sys.exit()
    pygame.display.update()

