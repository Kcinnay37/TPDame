import pygame
from Engine import Engine
from Player import Player
from AI import AI
from GameFlow import GameFlow
from Board import Board

class Game:
    isRun:bool

    width:int = 1000
    height:int = 800
    size:float = []

    screen:pygame.display.set_mode

    BGColor:int = [2, 0, 102]


    engine:Engine

    gameFlow:GameFlow

    player:Player
    AI:AI

    board:Board

    def __init__(self):
        self.isRun = True
        self.engine = Engine()
        self.gameFlow = GameFlow()
        pygame.init()
        self.GameInit()

    def GameInit(self):
        self.size = [self.width, self.height]
        self.screen = pygame.display.set_mode(self.size)

        self.board = Board("board", 5, self.size, 5)
        self.board.SetImagePath("Image\\WhitePawn.png", "Image\\WhiteKing.png", "Image\\BlackPawn.png", "Image\\BlackKing.png")

        self.engine.AddActor(self.board)

        self.player = Player("player", self.board)
        self.engine.AddActor(self.player)

        self.AI = AI("AI", self.board, 5)
        self.engine.AddActor(self.AI)

        self.engine.Start()

    def GameLoop(self):
        self.ProcessInput()

        self.engine.Update(0)

        self.Render()

        return self.isRun

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.player.SetClick(True)
                    self.player.SetMousePos(pygame.mouse.get_pos())




    def Render(self):
        self.screen.fill(self.BGColor)

        self.engine.Render(self.screen)

        pygame.display.flip()

    def ChangeDifficulty(self):
        self.AI.ChangeDifficulty()

    def RestartGame(self):
        self.board.RestartGame()
