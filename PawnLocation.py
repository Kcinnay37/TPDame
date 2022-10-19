from Grid import Grid
#from Actor import Actor
import copy
from Node import Node

class PawnLocation(Grid):

    def __init__(self, sizeX, sizeY, screenSizeX, screenSizeY, tag:str):
        super().__init__(sizeX, sizeY, screenSizeX, screenSizeY, tag)
        for i in range(self.sizeX * self.sizeY):
            self.grid.append(None)

    def ChangePos(self, posX1, posY1, posX2, posY2):
        pawn = self.grid[self.GetIndexAt(posX1, posY1)]
        pawn.SetGridPos(posX2, posY2)

        self.grid[self.GetIndexAt(posX1, posY1)] = None
        self.grid[self.GetIndexAt(posX2, posY2)] = pawn

    def EatPawnAt(self, x, y):
        pawn = self.grid[self.GetIndexAt(x, y)]
        pawn.SetIsDeath(True)
        self.grid[self.GetIndexAt(x, y)] = None

    def CheckCanJump(self, tag:str):
        value = [False, False]
        pos = []
        pawns = []

        for i in range(self.GetGridSize()):
            pawn = self.At(i)
            if pawn != None and pawn.GetTag() == tag:
                if pawn.GetTag() == "pawnPlayer" or (pawn.GetTag() == "pawnEnemy" and pawn.GetKing()):
                    index = pawn.GetIndexCornerRight(self, tag, False)
                    if index != None:
                        value[0] = True
                        if len(index) == 3:
                            value[1] = True
                        pos.append(index)
                        pawns.append(pawn)

                    index = pawn.GetIndexCornerLeft(self, tag, False)
                    if index != None:
                        value[0] = True
                        if  len(index) == 3:
                            value[1] = True
                        pos.append(index)
                        pawns.append(pawn)

                if pawn.GetTag() == "pawnEnemy" or (pawn.GetTag() == "pawnPlayer" and pawn.GetKing()):
                    index = pawn.GetIndexCornerLeftDown(self, tag, False)
                    if index != None:
                        value[0] = True
                        if len(index) == 3:
                            value[1] = True
                        pos.append(index)
                        pawns.append(pawn)

                    index = pawn.GetIndexCornerRightDown(self, tag, False)
                    if index != None:
                        value[0] = True
                        if len(index) == 3:
                            value[1] = True
                        pos.append(index)
                        pawns.append(pawn)

        return [value, [pos, pawns]]

    def Eat(self, initialPos, finalPos):
        nbEat:int = 0

        pos = initialPos
        if pos[0] > finalPos[0]:
            pos[0] -= 1
            nbEat = 1
        else:
            pos[0] += 1
            nbEat = 1

        if pos[1] > finalPos[1]:
            pos[1] -= 1
            nbEat = 1
        else:
            pos[1] += 1
            nbEat = 1

        while pos[0] != finalPos[0] and pos[1] != finalPos[1]:
            self.EatPawnAt(pos[0], pos[1])
            if pos[0] > finalPos[0]:
                pos[0] -= 1
            else:
                pos[0] += 1

            if pos[1] > finalPos[1]:
                pos[1] -= 1
            else:
                pos[1] += 1
            nbEat += 1
        return nbEat

    def GetAllMove(self, tag:str):
        nodes = []
        value = self.CheckCanJump(tag)

        if value[0][0] != False:
            for i in range(len(value[1][0])):
                if (value[0][1] and len(value[1][0][i]) == 3) or (not value[0][1]):

                    pointage:int = 1
                    pawnLocation = copy.deepcopy(self)
                    pawn = pawnLocation.At(pawnLocation.GetIndexAt(value[1][1][i].GetGridPos()[0], value[1][1][i].GetGridPos()[1]))

                    pointage += pawnLocation.Eat(pawn.GetGridPos(), [value[1][0][i][0], value[1][0][i][1]])
                    pawnLocation.ChangePos(pawn.GetGridPos()[0], pawn.GetGridPos()[1], value[1][0][i][0], value[1][0][i][1])

                    pawn.CheckIsKing()

                    if tag == "pawnPlayer":
                        pointage = -pointage
                        node = Node(pointage, pawnLocation, False)
                        nodes.append(node)
                    else:
                        node = Node(pointage, pawnLocation, True)
                        nodes.append(node)
            return nodes

        return None

    def Render(self, screen):
        for i in range(self.GetGridSize()):
            if self.At(i) != None:
                self.At(i).Render(screen)

#    def Update(self, dt:float):
#        for i in range(self.GetGridSize()):
#            if self.At(i) != None:
#                self.At(i).Update(dt)

    def __eq__(self, object):
        for i in range(self.GetGridSize()):
            if self.At(i) != object.At(i):
                return False
        return True
