import sys
import pygame
import time

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
DRAFT_WIDTH = PLAYER_HEIGHT
DRAFT_HEIGHT = DRAFT_WIDTH
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
    'Bottom':    (bp_x, bp_y),
    'Right':    (rp_x, rp_y),
    'Top':    (tp_x, tp_y),
    'Left':    (lp_x, lp_y)
}

StartBlockPositions = {
    'Bottom':    (BOARD_xend, BOARD_yend),
    'Right':    (BOARD_xend, BOARD_y-BLOCK_SIZE),
    'Top':    (BOARD_x-BLOCK_SIZE, BOARD_y-BLOCK_SIZE),
    'Left':    (BOARD_x-BLOCK_SIZE, BOARD_yend)
}

DraftPositions = {
    'Bottom':    (BOARD_xend+LARGE_MARGIN*2, BOARD_yend+LARGE_MARGIN*2),
    'Right':    (BOARD_xend+LARGE_MARGIN*2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2),
    'Top':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2),
    'Left':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2, BOARD_yend+LARGE_MARGIN*2)
}

DraftCenterPositions = {
    'Bottom':    (BOARD_xend+LARGE_MARGIN*2+DRAFT_WIDTH/2, BOARD_yend+LARGE_MARGIN*2+DRAFT_WIDTH/2),
    'Right':    (BOARD_xend+LARGE_MARGIN*2+DRAFT_WIDTH/2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2+DRAFT_WIDTH/2),
    'Top':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2+DRAFT_WIDTH/2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2+DRAFT_WIDTH/2),
    'Left':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2+DRAFT_WIDTH/2, BOARD_yend+LARGE_MARGIN*2+DRAFT_WIDTH/2)
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
        self.startblockposition = StartBlockPositions[self.position_name]
        self.draftposition = DraftPositions[self.position_name]
        self.index = list(PlayerPositions.keys()).index(self.position_name)
        self.pieces = self.createPieces()
        self.remaining = range(len(self.pieces))
    def createPieces(self):
        piecez = []
        for p in PIECES_ARR:
            piecez.append(Piece(p))
        return piecez
    
class Blokus(object):
    def __init__(self):
        self.players = self.createPlayers()

    def createPlayers(self):
        players = []
        players.append(Player(COLORS['RED'], 'Bottom'))
        players.append(Player(COLORS['GREEN'], 'Right'))
        players.append(Player(COLORS['BLUE'], 'Top'))
        players.append(Player(COLORS['YELLOW'], 'Left'))
        return players

class BlokusPyGame(Blokus):
    def __init__(self):
        super().__init__()
        self.window = None
        self.playerRegions = []
        self.startblocks = []
        self.draftRegions = []
        
    def initGUI(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.fill(COLORS['BLACK'])
                
        self.playBoard = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.playBoard.fill(COLORS['BLACK'])
        self.drawPlayBoard(self.playBoard)
        self.window.blit(self.playBoard, (BOARD_x, BOARD_y))
        
        self.playerRegions = []
        for i in range(4):
            new_player_region = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.playerRegions.append(new_player_region)
            new_player_region.fill(COLORS['BLACK'])
            self.drawPlayerRegion(new_player_region, self.players[i])
            new_player_region = pygame.transform.rotate(new_player_region, (90*i))
            self.window.blit(new_player_region, self.players[i].position)
        
        self.draftRegions = []
        for i in range(4):
            new_draft_region = pygame.Surface((DRAFT_WIDTH, DRAFT_HEIGHT))
            self.draftRegions.append(new_draft_region)
            new_draft_region.fill(COLORS['BLACK'])
            self.drawDraftRegion(new_draft_region, self.players[i])
            self.window.blit(new_draft_region, self.players[i].draftposition)
        
        self.startblocks = []
        for i in range(4):
            new_startblock = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.startblocks.append(new_startblock)
            self.drawStartBlock(new_startblock, self.players[i])
            self.window.blit(new_startblock, self.players[i].startblockposition)
    
    def updateGUI(self):
        self.window.blit(self.playBoard, (BOARD_x, BOARD_y))
        for i in range(4):
            self.window.blit(self.draftRegions[i], self.players[i].draftposition)
    
    def drawPlayerRegion(self, surface, player):
        rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        pygame.draw.rect(surface, player.color, rect, 1)
        for x in range(0, PLAYER_WIDTH, SMALL_PIECE_COMPART_SIZE):
            for y in range(0, PLAYER_HEIGHT, SMALL_PIECE_COMPART_SIZE):
                rect = pygame.Rect(x, y, SMALL_PIECE_COMPART_SIZE, SMALL_PIECE_COMPART_SIZE)
                pygame.draw.rect(surface, player.color, rect, 1)
        for x_ind in range(7):
            for y_ind in range(3):
                self.drawSmallPicece(surface, player.pieces[3*x_ind+y_ind], [SMALL_PIECE_COMPART_SIZE*(x_ind+0.6), SMALL_PIECE_COMPART_SIZE*(y_ind+0.6)], player.color)
    
    def drawDraftRegion(self, surface, player):
        surface.fill(COLORS['BLACK'])
        rect = pygame.Rect(0, 0, DRAFT_WIDTH, DRAFT_HEIGHT)
        pygame.draw.rect(surface, player.color, rect, 1)

    def drawPieceInDraft(self, player, piece_index):
        self.drawDraftRegion(self.draftRegions[player.index], player)
        center = [DRAFT_WIDTH/2, DRAFT_HEIGHT/2]
        self.drawPiece(self.draftRegions[player.index], player.pieces[piece_index], [center[0], center[1]], player.color)
    
    def drawPlayBoard(self, surface):
        for x in range(0, BOARD_WIDTH, BLOCK_SIZE):
            for y in range(0, BOARD_HEIGHT, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, COLORS["WHITE"], rect, 1)
    
    def drawBlock(self, surface, center, color):
        rect = pygame.Rect(center[0]-BLOCK_SIZE/2+1, center[1]-BLOCK_SIZE/2+1, BLOCK_SIZE-2, BLOCK_SIZE-2)
        pygame.draw.rect(surface, color, rect, 0)
    
    def drawSmallBlock(self, surface, center, color):
        rect = pygame.Rect(center[0]-SMALL_BLOCK_SIZE/2+1, center[1]-SMALL_BLOCK_SIZE/2+1, SMALL_BLOCK_SIZE-2, SMALL_BLOCK_SIZE-2)
        pygame.draw.rect(surface, color, rect, 0)
    
    def drawPiece(self, surface, piece, center, color):
        [dimx, dimy] = piece.dimension()
        for x_ind in range(dimx):
            x = center[0]+BLOCK_SIZE*(x_ind-dimx/2)
            for y_ind in range(dimy):
                y = center[1]+BLOCK_SIZE*(y_ind-dimy/2)
                if piece.piecearr[x_ind][y_ind] > 0:
                    self.drawBlock(surface, [x, y], color)
    
    def drawSmallPicece(self, surface, piece, center, color):
        [dimx, dimy] = piece.dimension()
        for x_ind in range(dimx):
            x = center[0]+SMALL_BLOCK_SIZE*(x_ind-dimx/2)
            for y_ind in range(dimy):
                y = center[1]+SMALL_BLOCK_SIZE*(y_ind-dimy/2)
                if piece.piecearr[x_ind][y_ind] > 0:
                    self.drawSmallBlock(surface, [x, y], color)
    
    def drawStartBlock(self, surface, player):
        surface.fill(player.color)
    
    def run(self):
        index = 0
        while True:
            self.drawPieceInDraft(self.players[0], index)
            self.updateGUI()
            time.sleep(0.5)
            index += 1
            if index > 20:
                index = 0
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
            pygame.display.update()      

        pygame.quit()
        sys.exit()
 
if __name__ == '__main__':
    bl = BlokusPyGame()
    bl.initGUI()
    bl.run()
    
