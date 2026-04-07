class Sudoku:
    def __init__(self):
        self.table = [[0 for i in range(9)] for j in range(9)]
    def initGame(self):
        self.table = [[0 for i in range(9)] for j in range(9)]
    def runGame(self):
        pass

class SudokuTk(Sudoku):
    def __init__(self):
        super().__init__()
    def initGame(self):
        super().initGame()
    def runGame(self):
        super().runGame()

if __name__ == '__main__':
    game = SudokuTk()
    game.initGame()
    game.runGame()
