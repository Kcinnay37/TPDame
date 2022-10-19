from Grid import Grid
import pygame

class Plateau(Grid):

    rect:pygame.Rect

    color:int = [222, 162, 33]
    color2:int = [153, 222, 33]

    def __init__(self, sizeX, sizeY, screenSizeX, screenSizeY, tag:str):
        super().__init__(sizeX, sizeY, screenSizeX, screenSizeY, tag)
        currValue:int = -1
        for i in range(self.sizeX * self.sizeY):
            if i % self.sizeX != 0:
                currValue = -currValue
            self.grid.append(currValue)


    def Render(self, screen):
        currPosX:int = -self.sizeGraphicX
        currPosY:int = -self.sizeGraphicY

        for i in range(self.sizeX * self.sizeY):
            if i % self.sizeX == 0:
                currPosY += self.sizeGraphicY
                currPosX = 0
            else:
                currPosX += self.sizeGraphicX

            if self.grid[i] == 1:
                self.rect = pygame.Rect(currPosX, currPosY, self.sizeGraphicX, self.sizeGraphicY)
                pygame.draw.rect(screen, pygame.Color(self.color), self.rect)
            elif self.grid[i] == 2:
                self.rect = pygame.Rect(currPosX, currPosY, self.sizeGraphicX, self.sizeGraphicY)
                pygame.draw.rect(screen, pygame.Color(self.color2), self.rect)
