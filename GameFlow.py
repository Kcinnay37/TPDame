# This Python file uses the following encoding: utf-8


class GameFlow:
    playerTurn:bool
    finish:bool


    def __init__(self):
        self.playerTurn = True
        self.finish = False

    def SetPlayerTurn(self, value:bool):
        self.playerTurn = value

    def GetPlayerTurn(self):
        return self.playerTurn

    def SetFinish(self, value:bool):
        self.finish = value

    def GetFinish(self):
        return self.finish
