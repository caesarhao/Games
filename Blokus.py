import pygame
SMALL_MARGIN = 1
MID_MARGIN = 5
LARGE_MARGIN = 10
BOARD_NUM_x = 20
BOARD_NUM_y = 20
BLOCK_SIZE = 20 # pixel
SMALL_BLOCK_SIZE = 10 # for player selection
SMALL_PIECE_COMPART_SIZE = (SMALL_BLOCK_SIZE*6)
BOARD_HEIGHT = (BLOCK_SIZE*BOARD_NUM_y)
BOARD_WIDTH = (BLOCK_SIZE*BOARD_NUM_x)
PLAYER_HEIGHT = 180
PLAYER_WIDTH = (BOARD_WIDTH+20)
BOARD_x = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2)
BOARD_xend = (BOARD_x+BOARD_WIDTH)
BOARD_y = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2)
BOARD_yend = (BOARD_y+BOARD_HEIGHT)
WINDOW_HEIGHT = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2+BOARD_HEIGHT+LARGE_MARGIN*2+PLAYER_HEIGHT+LARGE_MARGIN)
WINDOW_WIDTH = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2+BOARD_WIDTH+LARGE_MARGIN*2+PLAYER_HEIGHT+LARGE_MARGIN)


tp_x = BOARD_x - LARGE_MARGIN
tp_y = LARGE_MARGIN
lp_x = LARGE_MARGIN
lp_y = BOARD_y - LARGE_MARGIN
bp_x = BOARD_x - LARGE_MARGIN
bp_y = BOARD_yend + LARGE_MARGIN*2
rp_x = BOARD_xend + LARGE_MARGIN*2
rp_y = BOARD_y - LARGE_MARGIN


PlayerPositions = {
    'Top':    (tp_x, tp_y),
    'Left':    (lp_x, lp_y),
    'Bottom':    (bp_x, bp_y),
    'Right':    (rp_x, rp_y)
}
    
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
    def __init__(self, color, position_name):
        self.color = color
        self.position_name = position_name
        self.position = PlayerPositions[self.position_name]
        self.index = list(PlayerPositions.keys()).index(self.position_name)
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
        players.append(Player(COLORS['RED'], 'Top'))
        players.append(Player(COLORS['GREEN'], 'Left'))
        players.append(Player(COLORS['BLUE'], 'Bottom'))
        players.append(Player(COLORS['YELLOW'], 'Right'))
        return players

def drawInitPlayerRegion(surface, player):
    player_x = player.position[0]
    player_y = player.position[1]
    
    if player.index%2 == 0:
        real_pw = PLAYER_WIDTH
        real_ph = PLAYER_HEIGHT
    else:
        real_pw = PLAYER_HEIGHT
        real_ph = PLAYER_WIDTH
    rect = pygame.Rect(player_x, player_y, real_pw, real_ph)
    pygame.draw.rect(surface, player.color, rect, 1)
    for x in range(player_x, player_x+real_pw, SMALL_PIECE_COMPART_SIZE):
        for y in range(player_y, player_y+real_ph, SMALL_PIECE_COMPART_SIZE):
            rect = pygame.Rect(x, y, SMALL_PIECE_COMPART_SIZE, SMALL_PIECE_COMPART_SIZE)
            pygame.draw.rect(surface, player.color, rect, 1)
    # start block
    #rect = pygame.Rect(BOARD_x-BLOCK_SIZE, BOARD_y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    #pygame.draw.rect(surface, player.color, rect, 0)
 
if __name__ == '__main__':
    bl = Blokus()
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    
    # draw play Board
    for x in range(BOARD_x, BOARD_xend, BLOCK_SIZE):
        for y in range(BOARD_y, BOARD_yend, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(window, COLORS["WHITE"], rect, 1)
    
    # draw players regions
    # top player
    drawInitPlayerRegion(window, bl.players[0])
    rect = pygame.Rect(BOARD_x-BLOCK_SIZE, BOARD_y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, COLORS["RED"], rect, 0)
    # left player
    drawInitPlayerRegion(window, bl.players[1])
    rect = pygame.Rect(BOARD_x-BLOCK_SIZE, BOARD_yend, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, COLORS["GREEN"], rect, 0)
    
    # bottom player
    drawInitPlayerRegion(window, bl.players[2])
    rect = pygame.Rect(BOARD_xend, BOARD_yend, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, COLORS["BLUE"], rect, 0)
    
    # right player
    drawInitPlayerRegion(window, bl.players[3])
    rect = pygame.Rect(BOARD_xend, BOARD_y-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(window, COLORS["YELLOW"], rect, 0)
    
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        pygame.display.update()      

    pygame.quit()
    
