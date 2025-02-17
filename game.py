DEBUG_MODE = False

from func import *
import pygame 
from pygame.locals import *

pygame.init()
pygame.font.init()

from pathlib import Path

PATH = "/Users/peterlu/Desktop/sprites/"

"""
TODO 
add 2 player 4 player option
add wall
keys
"""

pygame.display.init()
scrn = pygame.display.set_mode(size = (662,556))

board = pygame.image.load(PATH + "board.png").convert()
piece1 = pygame.image.load(PATH + "piece1.png")
piece2 = pygame.image.load(PATH + "piece2.png")
piece3 = pygame.image.load(PATH + "piece3.png")
piece4 = pygame.image.load(PATH + "piece4.png")
options = pygame.image.load(PATH + "options.png")
wallH = pygame.image.load(PATH + "wallH.png")
wallV = pygame.image.load(PATH + "wallV.png")
test = pygame.image.load(PATH + "test.png")
nums = []
for i in range(11):
    nums.append(pygame.image.load(PATH + "num" + str(i) + ".png"))

#adjacency list for graph
boardGraph= createBoardList(9) 

"""
defaultXY: (250/10) (250/490)
stride: 60
"""

stride = 60
MinBound = 10
MaxBound = 490
WallShowX = 585
WallShowY = 195
WallLeft1 = WallLeft2 = 10

scrn.blit(board, (0, 0))
position1 = piece1.get_rect()
position1 = position1.move(250,MinBound)
scrn.blit(piece1, position1)
position3 = piece3.get_rect()
position3 = position3.move(250,MaxBound)
scrn.blit(piece3, position3)
positionW = nextWall = wallV.get_rect()

positionNum1 = nums[10].get_rect()
positionNum1 = positionNum1.move(WallShowX, WallShowY)
scrn.blit(nums[WallLeft1], positionNum1)
positionNum2 = nums[10].get_rect()
positionNum2 = positionNum2.move(WallShowX, WallShowY + 230)
scrn.blit(nums[WallLeft2], positionNum2)

pygame.display.flip()

#walls are 15 x 15 pixels

run = V = True
clicked = False

posList = [position1, position3]
pieceList = [piece1, piece3]
wallList = [(0,0,0,0)]
turn = 0

state = 0

while run:

    x, y = pygame.mouse.get_pos()

    modX = x % 60
    modY = y % 60
    wallX = (x-10) // 60 * 60 + 5
    wallY = (y-10) // 60 * 60 + 5
    onWall = False
    #showcase walls if mouse is on the wall spaces
    if x > 10 and y > 10 and x <= 490 and y <= 485 and modX > 5 and modX < 10 and not (modY > 5 and modY < 10):
        #hover wallV, add if clicked
        #scrn.blit(board, positionW, positionW)
        temp = wallV.get_rect()
        positionW = temp = temp.move(wallX + 60, wallY + 10)
        nextWall = temp.move(0,60)
        if positionW.collidelist(wallList) < 0:
            scrn.blit(wallV, temp)
            onWall = True
        temp = (0,0,0,0)
        V = True
    elif x > 10 and y > 10 and x < 485 and y <= 490 and modY > 5 and modY < 10 and not (modX > 5 and modX < 10):
        #hover wallH
        #scrn.blit(board, positionW, positionW)
        temp = wallH.get_rect()
        positionW = temp = temp.move(wallX + 10, wallY + 60)
        nextWall = temp.move(60,0)
        if positionW.collidelist(wallList) < 0:
            scrn.blit(wallH, temp)
            onWall = True
        temp = (0,0,0,0)
        V = False
    else:
        onWall = False
        #reset 
        if clicked:
            positionW = (0,0,0,0)
            clicked = False
        #if not clicked, delete previous wall:
        if positionW not in wallList and positionW.collidelist(wallList) < 0:
            scrn.blit(board, positionW, positionW)
        
    pygame.display.update()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and onWall:
            #check if wall blocks path
            if not update_graph(boardGraph, wall_to_ind(positionW, V), V, pos_to_ind(posList[turn]), (turn+1)%2): continue
            #update remaing wall count for player
            if turn == 0:
                if WallLeft1 == 0: continue
                WallLeft1 -= 1
                scrn.blit(board, positionNum1, positionNum1)
                scrn.blit(nums[WallLeft1], positionNum1)
            else:
                if WallLeft2 == 0: continue
                WallLeft2 -= 1
                scrn.blit(board, positionNum2, positionNum2)
                scrn.blit(nums[WallLeft2], positionNum2)
            wallList.append(positionW)

            if DEBUG_MODE:
                # print(wallList)
                print(f"wall_to_ind{wall_to_ind(positionW, V)}")
                # print(pos_to_ind(posList))
                # print(boardGraph)
                print(f"position wall {positionW}")
                print(f"player{turn}: {posList[turn]} - {pos_to_ind(posList[turn])}")
            

            #draw wall
            if V:
                scrn.blit(wallV, positionW)
            else:
                scrn.blit(wallH, positionW)
            #Do: update graph
            #updateGraph(V, wallX, wallY)
            pygame.display.update(positionW)
            clicked = True
            #update wall number 
            turn = (turn + 1) % 2
        if event.type == pygame.KEYDOWN:
            tempPos = posList[turn]

            moveList = [tempPos.move(-1*stride, 0), tempPos.move(stride, 0), tempPos.move(0, -1*stride), tempPos.move(0, stride)]

            #move a pixel to check wall presence
            checkWall = [tempPos.move(-1*5, 0), tempPos.move(5, 0), tempPos.move(0, -1*5), tempPos.move(0, 5)]


            moving = True
            if event.key == pygame.K_LEFT:
                if tempPos[0] <= MinBound: continue
                state = 0
                #matrix[px[0]][py[0]] = turn + 1
            elif event.key == pygame.K_RIGHT:
                if tempPos[0] >= MaxBound: continue
                state = 1
                #matrix[px[0]][py[0]] = turn + 1
            elif event.key == pygame.K_UP:
                if tempPos[1] <= MinBound: continue
                state = 2
                #matrix[px[0]][py[0]] = turn + 1
            elif event.key == pygame.K_DOWN:
                if tempPos[1] >= MaxBound: continue
                state = 3
                #matrix[px[0]][py[0]] = turn + 1
            else:
                moving = False
            
            if not moving:
                continue

            checkPos = checkWall[state]
            if checkPos.collidelist(wallList) >= 0: continue
        
            origin = tempPos.copy()
            tempPos = moveList[state]

            if DEBUG_MODE:
                print(f"checking: player{turn}: {tempPos}")



            hop = [tempPos.move(-1*stride, 0), tempPos.move(stride, 0), tempPos.move(0, -1*stride), tempPos.move(0, stride)]
            wtf = [tempPos.move(-1*5, 0), tempPos.move(5, 0), tempPos.move(0, -1*5), tempPos.move(0, 5)]
            if tempPos.colliderect(posList[(turn + 1) % 2]):
                rev = tempPos.copy()
                tempPos = wtf[state]
                if DEBUG_MODE:
                    print(wtf)
                    print(tempPos)
                if tempPos.collidelist(wallList) >= 0: 
                    tempPos = origin.copy()
                    continue
                tempPos = rev
                tempPos = hop[state]
                if outOfBounds(tempPos, MinBound, MaxBound):
                    tempPos = origin.copy()
                    continue

            scrn.blit(board, origin, origin)

            posList[turn] = tempPos
            if check_wincon(tempPos, turn):
                print(f"player{turn} wins")
                #add replay button
                run = False

            
            scrn.blit(pieceList[turn], tempPos)
            pygame.display.update()
            turn = (turn + 1) % 2



pygame.display.quit()
pygame.quit()

