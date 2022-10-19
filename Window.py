from Game import Game
from PySide6.QtWidgets import QWidget, QPushButton, QSlider
from PySide6.QtCore import QTimer

class Window(QWidget):
    game:Game
    timer:QTimer

    FPS:int

    def __init__(self, game:Game, FPS:int=60):
        super().__init__()
        self.FPS = 1000 / FPS
        self.InitUI()
        self.InitPygame(game)

    def InitUI(self):
        self.setWindowTitle("Interface Dame")
        self.setGeometry(10, 10, 300, 200)

        self.buttonDifficulty = QPushButton("ChangeDifficulty", self)
        self.buttonDifficulty.move(140, 70)
        self.buttonDifficulty.clicked.connect(self.ChangeDifficulty)

        self.buttonRestart = QPushButton("RestartGame", self)
        self.buttonRestart.move(60, 70)
        self.buttonRestart.clicked.connect(self.RestartGame)


        self.show()

    def InitPygame(self, game:Game):
        self.game = game

        self.timer = QTimer()
        self.timer.timeout.connect(self.IsRun)
        self.timer.start(self.FPS)

    def IsRun(self):
        if not self.game.GameLoop():
            self.close()

    def RestartGame(self):
        print("restart")
        self.game.RestartGame()

    def ChangeDifficulty(self):
        self.game.ChangeDifficulty()


