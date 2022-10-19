from GameFlow import GameFlow
from Actor import Actor
from Board import Board

class AI(Actor):
    depth:int
    board:Board

    difficulty:int

    def __init__(self, tag:str, board:Board, depth:int):
        super().__init__(tag)
        self.difficulty = 0
        self.depth = depth
        self.board = board

    def SetDifficulty(self, value:int):
        self.difficulty = value

    def Start(self):
        pass

    def Update(self, dt:float):
        if not self.board.GetGameFlow().GetPlayerTurn() and not self.board.GetGameFlow().GetFinish():

            match self.difficulty:
                case 0:
                    self.board.RandomMove()
                case 1:
                    self.board.BestMove(2)
                case 2:
                    self.board.BestMove(10)

            self.board.CheckBuildTree(self.board.GetGridPawn(), True, 10)

            self.board.CheckIsFinish()

            self.board.GetGameFlow().SetPlayerTurn(True)

    def ChangeDifficulty(self):
        if self.difficulty < 3:
            self.difficulty += 1
        else:
            self.difficulty = 0

        match self.difficulty:
            case 0:
                print("difficulte facile")
            case 1:
                print("difficulte moyen")
            case 2:
                print("difficulte difficile")

