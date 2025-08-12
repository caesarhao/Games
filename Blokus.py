import pygame
SMALL_MARGIN = 1
MID_MARGIN = 5
LARGE_MARGIN = 10
BOARD_NUM_x = 20
BOARD_NUM_y = 20
BLOCK_SIZE = 20 # pixel
BOARD_HEIGHT = (BLOCK_SIZE*BOARD_NUM_y)
BOARD_WIDTH = (BLOCK_SIZE*BOARD_NUM_x)
PLAYER_HEIGHT = 200
PLAYER_WIDTH = BOARD_WIDTH
BOARD_x = (LARGE_MARGIN+PLAYER_HEIGHT)
BOARD_xend = (BOARD_x+BOARD_WIDTH)
BOARD_y = (LARGE_MARGIN+PLAYER_HEIGHT)
BOARD_yend = (BOARD_y+BOARD_HEIGHT)
WINDOW_HEIGHT = (LARGE_MARGIN+PLAYER_HEIGHT+BOARD_HEIGHT+PLAYER_HEIGHT+LARGE_MARGIN)
WINDOW_WIDTH = (LARGE_MARGIN+PLAYER_HEIGHT+BOARD_WIDTH+PLAYER_HEIGHT+LARGE_MARGIN)


COLORS = {
    'BLACK':    (0,0,0),
    'WHITE':    (200,200,200),
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
        players.append(Player(COLORS['RED']))
        players.append(Player(COLORS['GREEN']))
        players.append(Player(COLORS['BLUE']))
        players.append(Player(COLORS['YELLOW']))
        return players
    
if __name__ == '__main__':
    bl = Blokus()
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    
    # draw players regions
    # top player
    tp_x = LARGE_MARGIN+PLAYER_HEIGHT
    ty_y = MID_MARGIN
    rect = pygame.Rect(tp_x, ty_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(window, COLORS["RED"], rect, 1)
    # left player
    lp_x = MID_MARGIN
    lp_y = LARGE_MARGIN+PLAYER_HEIGHT
    rect = pygame.Rect(lp_x, lp_y, PLAYER_HEIGHT, PLAYER_WIDTH)
    pygame.draw.rect(window, COLORS["GREEN"], rect, 1)
    # right player
    rp_x = WINDOW_WIDTH-PLAYER_HEIGHT-MID_MARGIN
    rp_y = LARGE_MARGIN+PLAYER_HEIGHT
    rect = pygame.Rect(rp_x, rp_y, PLAYER_HEIGHT, PLAYER_WIDTH)
    pygame.draw.rect(window, COLORS["BLUE"], rect, 1)
    # bottom player
    bp_x = LARGE_MARGIN+PLAYER_HEIGHT
    bp_y = WINDOW_HEIGHT-PLAYER_HEIGHT-MID_MARGIN
    rect = pygame.Rect(bp_x, bp_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(window, COLORS["YELLOW"], rect, 1)
    
    # draw play Board
    for x in range(LARGE_MARGIN+PLAYER_HEIGHT, WINDOW_WIDTH-PLAYER_HEIGHT-LARGE_MARGIN, BLOCK_SIZE):
        for y in range(LARGE_MARGIN+PLAYER_HEIGHT, WINDOW_HEIGHT-PLAYER_HEIGHT-LARGE_MARGIN, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(window, COLORS["WHITE"], rect, 1)
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        pygame.display.update()      

    pygame.quit()
    
