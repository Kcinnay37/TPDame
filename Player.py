from GameFlow import GameFlow
from Actor import Actor
from Board import Board

class Player(Actor):
    board:Board

    mousePos:float = []
    click:bool
    index:int = []

    colorIndex = []
    initialPose = []

    def __init__(self, tag:str, board:Board):
        super().__init__(tag)

        self.board = board

        self.mousePos = [0, 0]
        self.index = [0, 0]
        self.click = False

        self.colorIndex = []
        self.initialPose = []

    def Start(self):
        pass

    def Update(self, dt:float):
        if self.board.GetGameFlow().GetPlayerTurn() and not self.board.GetGameFlow().GetFinish():
            if self.click:
                self.SetIndex()
                if self.board.GetGridPawnAt(self.index) == self.board.GetPlayerNb()[0] or self.board.GetGridPawnAt(self.index) == self.board.GetPlayerNb()[1]:
                    if len(self.colorIndex) != 0:

                        self.board.ChangeColorIndex(self.colorIndex, '1')
                        self.colorIndex = []

                    self.board.CheckCanJump(self.board.GetGridPawn(), self.board.GetGameFlow().GetPlayerTurn())
                    moves = self.board.GetPossibleMove(self.index, self.board.GetGridPawn(), True)



                    self.board.ChangeColorIndex(moves, '2')
                    self.colorIndex = moves
                    self.initialPose = self.index

                else:

                    for i in range(len(self.colorIndex)):
                        if self.index[0] == self.colorIndex[i][0] and self.index[1] == self.colorIndex[i][1]:
                            newGrid = self.board.MovePawn(self.initialPose, self.colorIndex[i], self.board.GetGridPawn())

                            newGrid = newGrid[:len(newGrid) - 1] + 'p'

                            self.board.GridPawnEqual(newGrid)

                            self.board.CheckBuildTree(self.board.GetGridPawn(), False, 10)

                            self.board.CheckIsFinish()

                            self.board.ChangeColorIndex(self.colorIndex, '1')
                            self.colorIndex = []
                            self.initialPose = []

                            self.board.GetGameFlow().SetPlayerTurn(False)
                            break


            self.click = False


    def SetIndex(self):
        self.index = self.board.GetGridPosWithScreenLocation(self.mousePos)

    def SetMousePos(self, pos):
        self.mousePos = pos

    def SetClick(self, click:bool):
        self.click = click
