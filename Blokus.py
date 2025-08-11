import pygame

BOARD_HEIGHT = 20
BOARD_LENGTH = 20

COLORS = {
    'RED':      (255,0,0),
    'GREEN':    (0,255,0),
    'BLUE':     (0,0,255),
    'YELLOW':   (255,255,0)
    }

PIECES_ARR = [
        # 1*1
        [[1]],
        # 2*1
        [[1,1]],
        # 3*2
        [[1,1,1]],
        [[1,0],[1,1]],
        # 4*5
        [[1,1,1,1]],
        [[1,1],[1,1]],
        [[1,1,0],[0,1,1]],
        [[1,1,1],[1,0,0]],
        [[1,1,1],[0,1,0]],
        # 5*12
        [[1,1,1,1,1]],
        [[1,1,1,1],[1,0,0,0]],
        [[1,1,1,1],[0,1,0,0]],
        [[1,1,0,0],[0,1,1,1]],
        [[1,1,1],[1,1,0]],
        [[1,1,1],[1,0,1]],
        [[1,1,1],[1,0,0],[1,0,0]],
        [[1,1,1],[0,1,0],[0,1,0]],
        [[1,1,0],[0,1,1],[0,1,0]],
        [[1,1,0],[0,1,1],[0,0,1]],
        [[1,1,0],[0,1,0],[0,1,1]],
        [[0,1,0],[1,1,1],[0,1,0]]
    ]

class Piece:
    def __init__(self, piece_arr):
        self.piecearr = piece_arr.copy()
        
    def dimension(self):
        return [len(self.piecearr), len(self.piecearr[0])]
    def size(self):
        retu = 0
        for r in self.piecearr:
            for s in r:
                if s == 1:
                    retu += 1
        return retu
    def rotate(self):
        pass

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = self.createPieces()
        self.remaining = range(len(self.pieces))
    def createPieces(self):
        piecez = []
        for p in PIECES_ARR:
            piecez.append(Piece(p))
        return piecez
    
class Blokus:
    def __init__(self):
        self.players = self.createPlayers()

    def createPlayers(self):
        players = []
        players.append(Player('RED'))
        players.append(Player('GREEN'))
        players.append(Player('BLUE'))
        players.append(Player('YELLOW'))
        return players
    
if __name__ == '__main__':
    bl = Blokus()
    pygame.init()
    window = pygame.display.set_mode((640,480))
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        pygame.display.update()      

    pygame.quit()
    