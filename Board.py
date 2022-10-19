from Actor import Actor
from GameFlow import GameFlow
import pygame
import json
import random

class Board(Actor):
    tree = {}
    cost = {}

    grid:str
    gridPawn:str
    initialGridPawn:str

    playerPawnNb:int = '1'
    playerKingNb:int = '2'
    aiPawnNb:int = '3'
    aiKingNb:int = '4'

    currNbUnit:int = [0, 0]

    pathPawnPlayer:str
    pathKingPlayer:str

    pathPawnAI:str
    pathKingAI:str

    sizeBoard:int
    screenSize:int = []
    sizeGraphic:float = []

    color1:int = [222, 162, 33]
    color2:int = [153, 222, 33]

    gameFlow:GameFlow

    canJump:bool = False
    playerTurn:bool

    currCount:int = 0

    def __init__(self, tag:str, size:int, screenSize, nbUnit:int):
        self.grid = ""

        if size % 2 != 0:
            for i in range(size * size):
                if i % 2 == 0:
                    self.grid += '0'
                else:
                    self.grid += '1'
        else:
            currValue:str = '0'
            for i in range(size * size):
                if i % size != 0:
                    if currValue == '0':
                        currValue = '1'
                    else:
                        currValue = '0'

                self.grid += currValue

        self.sizeBoard = size

        self.screenSize = screenSize

        self.sizeGraphic = [float(self.screenSize[0] / self.sizeBoard), float(self.screenSize[1] / self.sizeBoard)]

        self.SetGridPawn(nbUnit)

        self.gameFlow = GameFlow()
        self.playerTurn = self.gameFlow.GetPlayerTurn()

        f1 = open("tree.json", "r")
        self.tree = json.load(f1)

        f2 = open("cost.json", "r")
        self.cost = json.load(f2)

        #self.CreateTree(28, self.gridPawn, True)

    def SetGridPawn(self, nbUnit):
        self.gridPawn = ""

        for c in self.grid:
            if c == '1':
                if self.currNbUnit[0] < nbUnit:
                    self.gridPawn += self.playerPawnNb
                    self.currNbUnit[0] += 1
                else:
                    self.gridPawn += '0'
            else:
                self.gridPawn += '0'

        self.gridPawn = self.gridPawn[::-1]

        index:int = 0
        for c in self.grid:
            if c == '1':
                if self.currNbUnit[1] < nbUnit:
                    self.gridPawn = self.gridPawn[:index] + self.aiPawnNb + self.gridPawn[index + 1:]
                    self.currNbUnit[1] += 1
                else:
                    break

            index += 1
        self.gridPawn += 'p'
        self.initialGridPawn = self.gridPawn
#        self.gridPawn = self.MovePawn([4, 1], [3, 2], self.gridPawn)

    def RestartGame(self):
        self.gridPawn = self.initialGridPawn

    def GridPawnEqual(self, gridPawn:str):
        self.gridPawn = gridPawn

    def SetImagePath(self, pathPawnPlayer:str, pathKingPlayer:str, pathPawnAI:str, pathKingAI:str):
        self.pathPawnPlayer = pathPawnPlayer
        self.pathKingPlayer = pathKingPlayer

        self.pathPawnAI = pathPawnAI
        self.pathKingAI = pathKingAI


    def GetGridPawn(self):
        return self.gridPawn
    def GetGridPosAt(self, i:int):
        posX:int = i % self.sizeBoard
        posY:int = int(i / self.sizeBoard)
        return [posX, posY]


    def GetScreenPosAt(self, pos:int):
        posX:int = self.sizeGraphic[0] * pos[0]
        posY:int = self.sizeGraphic[1] * pos[1]
        return [posX, posY]
    def GetGridPosWithScreenLocation(self, pos):
        posX:int = int(pos[0] / self.sizeGraphic[0])
        posY:int = int(pos[1] / self.sizeGraphic[1])
        return [posX, posY]

    def GetGridIndexAt(self, pos:int):
        #print(pos)
        index:int = self.sizeBoard * pos[1]
        index += pos[0]
        return index

    def GetGridPawnAt(self, pos:int):
        if pos[0] < 0 or pos[0] >= self.sizeBoard or pos[1] < 0 or pos[1] >= self.sizeBoard:
            return None

        return self.gridPawn[self.GetGridIndexAt(pos)]

    def GetGridAt(self, pos:int, grid:str):
        #print(pos)
        if pos[0] < 0 or pos[0] >= self.sizeBoard or pos[1] < 0 or pos[1] >= self.sizeBoard:
            return None

        return grid[self.GetGridIndexAt(pos)]

    def GetGridValueAt(self, pos:int):
        pass

    def GetPlayerNb(self):
        return [self.playerPawnNb, self.playerKingNb]
    def GetGameFlow(self):
        return self.gameFlow

    def GetFiveCornerIndex(self, pos:int):
        leftTopIndex:int = [pos[0] - 1, pos[1] - 1]
        rightTopIndex:int = [pos[0] + 1, pos[1] - 1]
        leftBotIndex:int = [pos[0] - 1, pos[1] + 1]
        rightBotIndex:int = [pos[0] + 1, pos[1] + 1]

        return [leftTopIndex, rightTopIndex, leftBotIndex, rightBotIndex, pos]

    def GetFiveCornerValue(self, pos:int, pawnBoard:str, playerTurn:bool):
        index = self.GetFiveCornerIndex(pos)

        leftTopValue:int = self.GetGridAt(index[0], pawnBoard)
        rightTopValue:int = self.GetGridAt(index[1], pawnBoard)
        leftBotValue:int = self.GetGridAt(index[2], pawnBoard)
        rightBotValue:int = self.GetGridAt(index[3], pawnBoard)

        enemyPawn:str = ""
        enemyKing:str = ""

        alliePawn:str = ""
        allieKing:str = ""

        currPawn = self.GetGridAt(index[4], pawnBoard)

        if playerTurn:
            enemyPawn = self.aiPawnNb
            enemyKing = self.aiKingNb
            alliePawn = self.playerPawnNb
            allieKing = self.playerKingNb
        else:
            enemyPawn = self.playerPawnNb
            enemyKing = self.playerKingNb
            alliePawn = self.aiPawnNb
            allieKing = self.aiKingNb

        if currPawn == self.playerPawnNb:
            leftBotValue = None
            rightBotValue = None

        if currPawn == self.aiPawnNb:
            leftTopValue = None
            rightTopValue = None

        values:str = []
        values.append(leftTopValue)
        values.append(rightTopValue)
        values.append(leftBotValue)
        values.append(rightBotValue)





        for i in range(len(values)):
            if values[i] != None and (values[i] == enemyPawn or values[i] == enemyKing):
                while(True):
                    if index[i][0] < index[4][0]:
                        index[i][0] -= 1
                    else:
                        index[i][0] += 1

                    if index[i][1] < index[4][1]:
                        index[i][1] -= 1
                    else:
                        index[i][1] += 1


                    values[i] = self.GetGridAt(index[i], pawnBoard)

                    if values[i] != None and (values[i] == alliePawn or values[i] == allieKing):
                        values[i] = None

                    if values[i] == None or (values[i] != enemyPawn and values[i] != enemyKing):
                        if values[i] != None:
                            self.canJump = True
                        break


        return [values, index]

    def GetPossibleMove(self, pos, pawnBoard:str, playerTurn):
        moveValues = self.GetFiveCornerValue(pos, pawnBoard, playerTurn)

        enemyPawn:str = ""
        enemyKing:str = ""

        alliePawn:str = ""
        allieKing:str = ""

        if playerTurn:
            enemyPawn = self.aiPawnNb
            enemyKing = self.aiKingNb
            alliePawn = self.playerPawnNb
            allieKing = self.playerKingNb
        else:
            enemyPawn = self.playerPawnNb
            enemyKing = self.playerKingNb
            alliePawn = self.aiPawnNb
            allieKing = self.aiKingNb

        possibleMove = []
        for i in range(len(moveValues[0])):
            if moveValues[0][i] != None and moveValues[0][i] != alliePawn and moveValues[0][i] != allieKing:
                if self.canJump:
                    distX = abs(moveValues[1][i][0] - moveValues[1][4][0])
                    distY = abs(moveValues[1][i][1] - moveValues[1][4][1])

                    if distX < 2 or distY < 2:
                        continue

                possibleMove.append(moveValues[1][i])

        return possibleMove



    def AddStep(self, currPawnGrid):
        self.CheckCanJump(currPawnGrid, self.playerTurn)

        allMove = []
        index:int = 0
        for c in currPawnGrid:
            if (c == self.playerPawnNb or c == self.playerKingNb) and self.playerTurn:
                move = self.GetPossibleMove(self.GetGridPosAt(index), currPawnGrid, self.playerTurn)
                if move != []:
                    for i in range(len(move)):
                        allMove.append(self.GetGridPosAt(index))
                        allMove.append(move[i])
            elif(c == self.aiPawnNb or c == self.aiKingNb) and not self.playerTurn:
                move = self.GetPossibleMove(self.GetGridPosAt(index), currPawnGrid, self.playerTurn)
                if move != []:
                    for i in range(len(move)):
                        allMove.append(self.GetGridPosAt(index))
                        allMove.append(move[i])

            index += 1

        possibility = []

        for i in range(0, len(allMove), 2):
            self.currCount = 0
            grid = self.MovePawn(allMove[i], allMove[i + 1], currPawnGrid)

            if self.playerTurn:
                grid = grid[:len(grid) - 1] + 'p'
            else:
                grid = grid[:len(grid) - 1] + 'e'

            if not grid in self.cost:
                if self.playerTurn:
                    self.cost[grid] = -self.currCount
                else:
                    self.cost[grid] = self.currCount

            possibility.append(grid)

        self.tree[currPawnGrid] = possibility
        self.canJump = False


    def CreateTree(self, depth, initialPawnGrid, playerTurn:bool):
        self.playerTurn = playerTurn

        parentGrid:str = []
        parentGrid.append(initialPawnGrid)

        for i in range(depth):
            childGrid:str = []
            for p in range(len(parentGrid)):
                if not parentGrid[p] in self.tree:
                    self.AddStep(parentGrid[p])
                    for e in range(len(self.tree[parentGrid[p]])):
                        childGrid.append(self.tree[parentGrid[p]][e])
                    if len(self.tree[parentGrid[p]]) == 0:
                        if self.playerTurn:
                            self.cost[parentGrid[p]] = 100
                        else:
                            self.cost[parentGrid[p]] = -100

            parentGrid = childGrid
            self.playerTurn = not self.playerTurn

            if len(parentGrid) == 0:
                break

        f1 = open("tree.json", "w")
        json.dump(self.tree, f1, indent = 3)

        f2 = open("cost.json", "w")
        json.dump(self.cost, f2, indent = 3)

    def CheckCanJump(self, pawnBoard:str, playerTurn:bool):
        enemyPawn:str = ""
        enemyKing:str = ""

        alliePawn:str = ""
        allieKing:str = ""

        if playerTurn:
            enemyPawn = self.aiPawnNb
            enemyKing = self.aiKingNb
            alliePawn = self.playerPawnNb
            allieKing = self.playerKingNb
        else:
            enemyPawn = self.playerPawnNb
            enemyKing = self.playerKingNb
            alliePawn = self.aiPawnNb
            allieKing = self.aiKingNb

        index:int = 0
        for c in pawnBoard:
            if c == alliePawn or c == allieKing:
                self.GetFiveCornerValue(self.GetGridPosAt(index), pawnBoard, playerTurn)
            if self.canJump:
                break
            index += 1

    def CheckIsFinish(self):
        if len(self.tree[self.gridPawn]) == 0:
            self.gameFlow.SetFinish(True)
            print("feni")

    def CheckBuildTree(self, gridPawn, playerTurn, depth:int):
        if not gridPawn in self.tree:
            self.CreateTree(depth, gridPawn, playerTurn)

    def MovePawn(self, pos1:int, pos2:int, pawnBoard:str):
        index1 = self.GetGridIndexAt(pos1)
        index2 = self.GetGridIndexAt(pos2)

        pawn:str = self.GetGridAt(pos1, pawnBoard)
        if (pos2[1] == 0 and pawn == self.playerPawnNb):
            pawn = self.playerKingNb
            self.currCount += 3
        if(pos2[1] == self.sizeBoard - 1 and pawn == self.aiPawnNb):
            pawn = self.aiKingNb
            self.currCount += 3

        pawnBoard = pawnBoard[:index2] + pawn + pawnBoard[index2 + 1:]
        pawnBoard = pawnBoard[:index1] + '0' + pawnBoard[index1 + 1:]

        self.canJump = False

        pawnBoard = self.Eat(pos1, pos2, pawnBoard)
        return pawnBoard

    def BestMove(self, depth:int):
        self.initialDepth = depth
        self.minimax(self.gridPawn, self.initialDepth, True)

        if len(self.tree[self.gridPawn]) != 0:
            self.gridPawn = self.tree[self.gridPawn][self.indexMove]

    def RandomMove(self):
        index = random.randint(0, len(self.tree[self.gridPawn]) - 1)
        if len(self.tree[self.gridPawn]) != 0:
            self.gridPawn = self.tree[self.gridPawn][index]

    initialDepth:int
    indexMove:int
    def minimax(self, gridPawn, depth, maximising):
        self.CheckBuildTree(gridPawn, not maximising, depth + 1)

        if depth == 0 or self.cost[gridPawn] == -100 or self.cost[gridPawn] == 100:
            return self.cost[gridPawn]
        if maximising:
            value = -9999999999
            oldValue = value
            for child in range(len(self.tree[gridPawn])):
                value = max(value, self.minimax(self.tree[gridPawn][child], depth - 1, False))

                if depth == self.initialDepth:
                    if value > oldValue:
                        self.oldValue = value
                        self.indexMove = child

            return value
        else:
            value = 9999999999
            oldValue = value
            for child in range(len(self.tree[gridPawn])):
                value = min(value, self.minimax(self.tree[gridPawn][child], depth - 1, True))

                if depth == self.initialDepth:
                    if value < oldValue:
                        self.oldValue = value
                        self.indexMove = child

            return value


    def ChangeColorIndex(self, index, value:str):
        for i in range(len(index)):
            place = self.GetGridIndexAt(index[i])
            self.grid = self.grid[:place] + value + self.grid[place + 1:]

    def Eat(self, pos1:int, pos2:int, pawnBoard:str):
        nbEat:int = 0

        while pos1[0] != pos2[0] and pos1[1] != pos2[1]:
            index = self.GetGridIndexAt(pos1)
            pawnBoard = pawnBoard[:index] + '0' + pawnBoard[index + 1:]

            if pos1[0] > pos2[0]:
                pos1[0] -= 1
            else:
                pos1[0] += 1

            if pos1[1] > pos2[1]:
                pos1[1] -= 1
            else:
                pos1[1] += 1
            nbEat += 1


        self.currCount += nbEat
        return pawnBoard


    def Render(self, screen):
        currPos:float = [-self.sizeGraphic[0], -self.sizeGraphic[1]]

        index:int = 0
        for c in self.grid:
            if index % self.sizeBoard == 0:
                currPos[1] += self.sizeGraphic[1]
                currPos[0] = 0
            else:
                currPos[0] += self.sizeGraphic[0]

            if c == '1':
                self.rect = pygame.Rect(currPos[0], currPos[1], self.sizeGraphic[0], self.sizeGraphic[1])
                pygame.draw.rect(screen, pygame.Color(self.color1), self.rect)
            elif c == '2':
                self.rect = pygame.Rect(currPos[0], currPos[1], self.sizeGraphic[0], self.sizeGraphic[1])
                pygame.draw.rect(screen, pygame.Color(self.color2), self.rect)

            index += 1

        index = 0
        for c in self.gridPawn:
            if c != '0' and c != 'p' and c != 'e':
                img:pygame.image.load = None
                if c == self.aiPawnNb:
                    img = pygame.image.load(self.pathPawnAI)
                elif c == self.aiKingNb:
                    img = pygame.image.load(self.pathKingAI)
                elif c == self.playerPawnNb:
                    img = pygame.image.load(self.pathPawnPlayer)
                elif c == self.playerKingNb:
                    img = pygame.image.load(self.pathKingPlayer)


                img = pygame.transform.scale(img, self.sizeGraphic)
                screen.blit(img, self.GetScreenPosAt(self.GetGridPosAt(index)))

            index += 1
    def PrintBoard(self, board):
        count:int = 0
        for c in board:
            if count < 4:
                print(c, end='')
            else:
                print(c)
                count = 0
                continue

            count += 1
        print('')
