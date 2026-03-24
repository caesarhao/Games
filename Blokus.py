import math
import sys
import pygame
import time
import numpy

SMALL_MARGIN = 1
MID_MARGIN = 5
LARGE_MARGIN = 10
BOARD_NUM_x = 20
BOARD_NUM_y = BOARD_NUM_x
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
INFO_REGION_HEIGHT = 200
WINDOW_HEIGHT = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2+BOARD_HEIGHT+LARGE_MARGIN*2+PLAYER_HEIGHT+LARGE_MARGIN+INFO_REGION_HEIGHT)
WINDOW_WIDTH = (LARGE_MARGIN+PLAYER_HEIGHT+LARGE_MARGIN*2+BOARD_WIDTH+LARGE_MARGIN*2+PLAYER_HEIGHT+LARGE_MARGIN)

# the board is the base to calculate the position of other regions, so the position of the board is fixed.
# the top-left position of each player region is based on the position of the board.
# top player region is on the top of the board
tp_x = BOARD_x - LARGE_MARGIN
tp_y = BOARD_y - LARGE_MARGIN*2 - PLAYER_HEIGHT
# left player region is on the left of the board
lp_x = BOARD_x - LARGE_MARGIN*2 - PLAYER_HEIGHT
lp_y = BOARD_y - LARGE_MARGIN
# bottom player region is on the bottom of the board
bp_x = BOARD_x - LARGE_MARGIN
bp_y = BOARD_yend + LARGE_MARGIN*2
# right player region is on the right of the board
rp_x = BOARD_xend + LARGE_MARGIN*2
rp_y = BOARD_y - LARGE_MARGIN

# the position of each player region
PlayerPositions = {
    'Bottom':    (bp_x, bp_y),
    'Right':    (rp_x, rp_y),
    'Top':    (tp_x, tp_y),
    'Left':    (lp_x, lp_y)
}

GuideBlockPositions = {
    'Bottom':    (BOARD_xend, BOARD_yend),
    'Right':    (BOARD_xend, BOARD_y-BLOCK_SIZE),
    'Top':    (BOARD_x-BLOCK_SIZE, BOARD_y-BLOCK_SIZE),
    'Left':    (BOARD_x-BLOCK_SIZE, BOARD_yend)
}

StartBlockIndexes = {
    'Bottom':    (BOARD_NUM_x - 1, BOARD_NUM_y - 1),
    'Right' :    (BOARD_NUM_x - 1, 0),
    'Top'   :    (0, 0),
    'Left'  :    (0, BOARD_NUM_y - 1)
}

# the position of each player draft region
DraftPositions = {
    'Bottom':    (BOARD_xend+LARGE_MARGIN*2, BOARD_yend+LARGE_MARGIN*2),
    'Right':    (BOARD_xend+LARGE_MARGIN*2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2),
    'Top':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2, BOARD_y-DRAFT_HEIGHT-LARGE_MARGIN*2),
    'Left':    (BOARD_x-DRAFT_HEIGHT-LARGE_MARGIN*2, BOARD_yend+LARGE_MARGIN*2)
}

# the center position of each player draft region
DraftCenterPositions = {
    'Bottom':    (DraftPositions['Bottom'][0]+DRAFT_WIDTH/2, DraftPositions['Bottom'][1]+DRAFT_WIDTH/2),
    'Right':    (DraftPositions['Right'][0]+DRAFT_WIDTH/2, DraftPositions['Right'][1]+DRAFT_WIDTH/2),
    'Top':    (DraftPositions['Top'][0]+DRAFT_WIDTH/2, DraftPositions['Top'][1]+DRAFT_WIDTH/2),
    'Left':    (DraftPositions['Left'][0]+DRAFT_WIDTH/2, DraftPositions['Left'][1]+DRAFT_WIDTH/2)
}

# defition of colors    
COLORS = {
    'BLACK':    (0,0,0),
    'GRAY':     (128,128,128),
    'WHITE':    (200,200,200),
    'RED':      (255,0,0),
    'GREEN':    (0,255,0),
    'BLUE':     (0,0,255),
    'YELLOW':   (255,255,0)
    }

# the definition of pieces, 21 pieces in total, each piece is represented by a 2D array, where 1 means there is a block and 0 means there is no block.
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
    '''
        the definition of the Piece class, which represents a piece in the game, it has the following attributes:
        piecearr: the original 2D array of the piece, which is used to calculate the variants of the piece, and to calculate the number of blocks in the piece.
        variants: a list of 2D arrays, which are the variants of the piece, including the original piece, the rotated pieces and the flipped pieces. there are at most 8 variants for each piece, but some pieces have less than 8 variants because of the symmetry.
        idx: the index of the current variant of the piece, which is used to keep track of the current variant of the piece when the player rotates the piece in the draft region.
    '''
    STATUS_InStock = 0
    STATUS_InDraft = 1
    STATUS_InBoard = 2
    def __init__(self, piece_arr):
        self.__piecearr = piece_arr.copy()
        self.variants = []
        self.cal_variants()
        self.__idx = 0
        self.status = Piece.STATUS_InStock
    def num_of_variants(self):
        return len(self.variants)
    def curent_idx(self):
        return self.__idx
    def current_variant(self):
        return self.variants[self.__idx]
    def ini_variant(self):
        return self.variants[0]
    def next_variant(self):
        self.__idx += 1
        if self.__idx >= self.num_of_variants():
            self.__idx = 0
        return self.variants[self.__idx]
    def previous_variant(self):
        self.__idx -= 1
        if self.__idx < 0:
            self.__idx = self.num_of_variants() - 1
        return self.variants[self.__idx]
    def ini_shape(self):
        return (len(self.__piecearr), len(self.__piecearr[0]))
    def current_shape(self):
        return (len(self.current_variant()), len(self.current_variant()[0]))
    def num_of_blocks(self):
        return numpy.count_nonzero(self.__piecearr)
    def rot90Left(self, pa, k):
        return numpy.rot90(pa, k).tolist()
    def rot90Right(self, pa, k):
        return numpy.rot90(pa, -k).tolist()
    def flipud(self, pa):
        return numpy.flipud(pa).tolist()
    def fliplr(self, pa):
        return numpy.fliplr(pa).tolist()
    def serialize_variant(variant) -> str:
        retu = ''
        for row in variant:
            for col in row:
                retu += (str(col) + ',')
            retu += ';'
        return retu
    def deserialize_variant(string):
        rows = string.split(';')
        rows.pop()
        retu = []
        for r in rows:
            rl = r.split(',')
            rl.pop()
            rl = list(map(int, rl))
            retu.append(rl)
        return retu
        
    def cal_variants(self):
        self.variants = []
        for i in range(4):
            self.variants.append(self.rot90Left(self.__piecearr, i))
        piecearr_ud = self.flipud(self.__piecearr)
        for i in range(4):
            self.variants.append(self.rot90Left(piecearr_ud, i))
        # remove duplicates
        variants_str_list = list(map(Piece.serialize_variant, self.variants))
        variants_str_list = list(dict.fromkeys(variants_str_list))
        self.variants = list(map(Piece.deserialize_variant, variants_str_list))

class Player:
    '''
    the definition of the Player class, which represents a player in the game, it has the following attributes:
color: the color of the player, which is used to draw the pieces of the player on the board and in the player region.
position_name: the name of the position of the player, which is used to calculate the position of the player region, the draft region and the start block.
position: the position of the player region, which is used to draw the player region on the window.
startblockposition: the position of the start block, which is used to draw the start block on the window.
draftposition: the position of the draft region, which is used to draw the draft region on the window.
index: the index of the player, which is used to access the player region surface and the draft region surface in the BlokusPyGame class.
pieces: a list of Piece objects, which are the pieces of the player, and the status of each piece is stored in the Piece object, which is used to draw the pieces in the player region and the draft region.
remaining: a list of the indices of the pieces that are still in stock, which is used to keep track of the pieces that are still in stock, and to check if the player has any pieces left to play.'''
    def __init__(self, color, position_name):
        self.color = color
        self.position_name = position_name
        self.position = PlayerPositions[self.position_name]
        self.guideblockposition = GuideBlockPositions[self.position_name]
        self.draftposition = DraftPositions[self.position_name]
        self.index = list(PlayerPositions.keys()).index(self.position_name)
        self.pieces = self.createPieces()
        self.remaining = list(range(len(self.pieces)))
    def createPieces(self):
        piecez = []
        for p in PIECES_ARR:
            piecez.append(Piece(p))
        return piecez
    def current_piece(self):
        for i in range(len(self.pieces)):
            if self.pieces[i].status == Piece.STATUS_InDraft:
                return self.pieces[i]
        return None
    def current_piece_index(self):
        for i in range(len(self.pieces)):
            if self.pieces[i].status == Piece.STATUS_InDraft:
                return i
        return None
    def remove_piece_from_remaining(self, piece_index):
        if piece_index in self.remaining:
            self.remaining.remove(piece_index)
    
class Board:
    '''
    the definition of the Board class, which represents the board in the game, it has the following attributes:
    the board is represented by a 2D array, where -1 means there is no piece on the block, and 0, 1, 2, 3 means there is a piece of the player with index 0, 1, 2, 3 on the block respectively. the board is used to check if the piece can be placed on the board, and to draw the pieces on the board.
    '''
    def __init__(self):
        self.table = [[-1 for i in range(BOARD_NUM_x)] for j in range(BOARD_NUM_y)]
        self.table4display = [[-1 for i in range(BOARD_NUM_x)] for j in range(BOARD_NUM_y)]
    
    def resetTable4Display(self):
        for i in range(BOARD_NUM_x):
            for j in range(BOARD_NUM_y):
                self.table4display[i][j] = self.table[i][j]
    
    def updateTable(self, blockIndexes, player_index, piece2display : Piece):
        x_ind = blockIndexes[0]
        y_ind = blockIndexes[1]
        value = player_index
        dim_x = piece2display.current_shape()[0]
        dim_y = piece2display.current_shape()[1]
        if x_ind + dim_x > BOARD_NUM_x or y_ind + dim_y > BOARD_NUM_y:
            return
        for i in range(dim_x):
            for j in range(dim_y):
                if piece2display.current_variant()[i][j] > 0:
                    self.table[x_ind+i][y_ind+j] = value
    
    def updateDisplayTable(self, blockIndexes, player_index, piece2display : Piece):
        x_ind = blockIndexes[0]
        y_ind = blockIndexes[1]
        value = player_index
        dim_x = piece2display.current_shape()[0]
        dim_y = piece2display.current_shape()[1]
        if x_ind + dim_x > BOARD_NUM_x or y_ind + dim_y > BOARD_NUM_y:
            return
        for i in range(dim_x):
            for j in range(dim_y):
                if piece2display.current_variant()[i][j] > 0:
                    self.table4display[x_ind+i][y_ind+j] = value
    
    def validatePotentialPlacement(self, blockIndexes, player, piece2place : Piece) -> bool:
        # check if the piece can be placed on the board according to the rules of the game, which are:
        x_ind = blockIndexes[0]
        y_ind = blockIndexes[1]
        dim_x = piece2place.current_shape()[0]
        dim_y = piece2place.current_shape()[1]
        player_index = player.index
        # 0. the first piece of each player must be placed in the corner of the board, and the start block of each player is defined in the StartBlockIndexes dictionary, which is based on the position of the player region.
        if len(player.remaining) == len(player.pieces):
            start_block_index = StartBlockIndexes[player.position_name]
            for i in range(dim_x):
                for j in range(dim_y):
                    if piece2place.current_variant()[i][j] > 0:
                        if (x_ind+i, y_ind+j) == start_block_index:
                            return True
        # 1. the piece must be placed on the board, and cannot be placed outside the board.
        if x_ind + dim_x > BOARD_NUM_x or y_ind + dim_y > BOARD_NUM_y:
            return False
         # 2. the piece cannot be placed on top of another piece.
        for i in range(dim_x):
            for j in range(dim_y):
                if piece2place.current_variant()[i][j] > 0 and self.table[x_ind+i][y_ind+j] > -1:
                    return False
        # 3. the piece must be placed in a way that it touches at least the corner of a piece of the same player, but cannot touch any piece of the same player by edge, it can only touch by corner.
        touch_corner = False
        for i in range(dim_x):
            for j in range(dim_y):
                if piece2place.current_variant()[i][j] > 0:
                    # check the 4 corners of the block
                    if (x_ind+i-1 >= 0 and y_ind+j-1 >= 0 and self.table[x_ind+i-1][y_ind+j-1] == player_index) or \
                       (x_ind+i-1 >= 0 and y_ind+j+1 < BOARD_NUM_y and self.table[x_ind+i-1][y_ind+j+1] == player_index) or \
                       (x_ind+i+1 < BOARD_NUM_x and y_ind+j-1 >= 0 and self.table[x_ind+i+1][y_ind+j-1] == player_index) or \
                       (x_ind+i+1 < BOARD_NUM_x and y_ind+j+1 < BOARD_NUM_y and self.table[x_ind+i+1][y_ind+j+1] == player_index):
                        touch_corner = True
                    # check the 4 edges of the block
                    if (x_ind+i-1 >= 0 and self.table[x_ind+i-1][y_ind+j] == player_index) or \
                       (x_ind+i+1 < BOARD_NUM_x and self.table[x_ind+i+1][y_ind+j] == player_index) or \
                       (y_ind+j-1 >= 0 and self.table[x_ind+i][y_ind+j-1] == player_index) or \
                       (y_ind+j+1 < BOARD_NUM_y and self.table[x_ind+i][y_ind+j+1] == player_index):
                        return False
        return touch_corner

class Blokus(object):
    STATUS_InStock = 0
    STATUS_InDraft = 1
    STATUS_InBoard = 2
    def __init__(self):
        self.board = Board()
        self.players = self.createPlayers()
        self.current_player_index = 0
        self.PlayerStatus = Blokus.STATUS_InStock

    def createPlayers(self):
        players = []
        players.append(Player(COLORS['RED'], 'Bottom'))
        players.append(Player(COLORS['GREEN'], 'Right'))
        players.append(Player(COLORS['BLUE'], 'Top'))
        players.append(Player(COLORS['YELLOW'], 'Left'))
        return players
    
    def getColorWithPlayerIndex(self, index):
        return self.players[index].color

    def nextPlayer(self):
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0


class BlokusPyGame(Blokus):
    def __init__(self):
        super().__init__()
        self.screen = None
        self.dest_width = WINDOW_WIDTH
        self.dest_height = WINDOW_HEIGHT
        self.scale = 1
        self.window = None
        self.playBoard = None
        self.playBoardRect = None
        self.playerRegionSurfaces = []
        self.playerRegionRects = []
        self.playerPiecesRects = []
        self.draftRegionSurfaces = []
        self.draftRegionRects = []
        self.guideBlockSurfaces = []
        self.guideBlockRects = []
        self.blockIndexesOnBoard = (-1, -1)
        
    def initGUI(self):
        pygame.init()
        screen_info = pygame.display.Info()
        # print(screen_info)
        self.dest_height = screen_info.current_h * 0.8
        self.scale = WINDOW_HEIGHT/self.dest_height
        self.dest_width = WINDOW_WIDTH/self.scale
        print("Display scale is " + str(self.scale))
        self.screen = pygame.display.set_mode((self.dest_width, self.dest_height), pygame.SCALED)
        pygame.display.set_caption("Blokus")        
        self.window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.fill(COLORS['BLACK'])
 
        self.playBoardRect = pygame.Rect(BOARD_x, BOARD_y, BOARD_WIDTH, BOARD_HEIGHT)
        self.playBoard = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.playBoard.fill(COLORS['BLACK'])
        self.drawPlayBoard()
        self.window.blit(self.playBoard, (BOARD_x, BOARD_y))
        
        self.playerRegionSurfaces = []
        for i in range(4):
            if i%2 == 0:
                rw = PLAYER_WIDTH
                rh = PLAYER_HEIGHT
            else:
                rh = PLAYER_WIDTH
                rw = PLAYER_HEIGHT 
            new_player_region = pygame.Surface((rw, rh))
            self.playerRegionSurfaces.append(new_player_region)
            new_player_region.fill(COLORS['BLACK'])
            self.drawPlayerRegion(self.players[i])
            
            self.window.blit(new_player_region, self.players[i].position)
            new_player_region_rect = pygame.Rect(self.players[i].position[0], self.players[i].position[1], rw, rh)
            self.playerRegionRects.append(new_player_region_rect)
            self.playerPiecesRects.append([])
            if i%2 == 0:
                row_num = 3
                col_num = 7
            else:
                row_num = 7
                col_num = 3
            for y_ind in range(row_num):
                for x_ind in range(col_num):
                    new_piece_rect = pygame.Rect(self.players[i].position[0]+SMALL_PIECE_COMPART_SIZE*x_ind, self.players[i].position[1]++SMALL_PIECE_COMPART_SIZE*y_ind, SMALL_PIECE_COMPART_SIZE, SMALL_PIECE_COMPART_SIZE)
                    self.playerPiecesRects[i].append(new_piece_rect)
            
        
        self.draftRegionSurfaces = []
        for i in range(4):
            new_draft_region = pygame.Surface((DRAFT_WIDTH, DRAFT_HEIGHT))
            self.draftRegionSurfaces.append(new_draft_region)
            new_draft_region.fill(COLORS['BLACK'])
            self.drawDraftRegion(self.players[i])
            self.window.blit(new_draft_region, self.players[i].draftposition)
            new_draft_region_rect = pygame.Rect(self.players[i].draftposition[0], self.players[i].draftposition[1], DRAFT_WIDTH, DRAFT_HEIGHT)
            self.draftRegionRects.append(new_draft_region_rect)
        
        self.guideBlockSurfaces = []
        for i in range(4):
            new_guideblock = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.guideBlockSurfaces.append(new_guideblock)
            self.drawGuideBlock(self.players[i])
            self.window.blit(new_guideblock, self.players[i].guideblockposition)
        
        scaled_window = pygame.transform.scale(self.window, (self.dest_width, self.dest_height))
        self.screen.blit(scaled_window, (0,0))
        pygame.display.update() 
    
    def updateGUI(self):
        for i in range(4):
            self.window.blit(self.playerRegionSurfaces[i], self.players[i].position)
            self.window.blit(self.guideBlockSurfaces[i], self.players[i].guideblockposition)
            self.window.blit(self.draftRegionSurfaces[i], self.players[i].draftposition)
        self.window.blit(self.playBoard, (BOARD_x, BOARD_y))
        scaled_window = pygame.transform.scale(self.window, (self.dest_width, self.dest_height))
        self.screen.blit(scaled_window, (0,0))
        pygame.display.update()

    def drawPlayerRegion(self, player : Player):
        surface = self.playerRegionSurfaces[player.index]
        surface.fill(COLORS['BLACK'])
        if player.index%2 == 0: 
            rw = PLAYER_WIDTH
            rh = PLAYER_HEIGHT
            row_num = 3
            col_num = 7
        else:
            rh = PLAYER_WIDTH
            rw = PLAYER_HEIGHT
            row_num = 7
            col_num = 3 
        rect = pygame.Rect(0, 0, rw, rh)
        pygame.draw.rect(surface, player.color, rect, 2)
        for x in range(0, rw, SMALL_PIECE_COMPART_SIZE):
            for y in range(0, rh, SMALL_PIECE_COMPART_SIZE):
                rect = pygame.Rect(x, y, SMALL_PIECE_COMPART_SIZE, SMALL_PIECE_COMPART_SIZE)
                pygame.draw.rect(surface, player.color, rect, 2)
        for y_ind in range(row_num):
            for x_ind in range(col_num):
                color = player.color
                if player.pieces[col_num*y_ind+x_ind].status != Piece.STATUS_InStock:
                    color = COLORS['GRAY']
                self.drawSmallPicece(surface, player.pieces[col_num*y_ind+x_ind], [SMALL_PIECE_COMPART_SIZE*(x_ind+0.5), SMALL_PIECE_COMPART_SIZE*(y_ind+0.5)], color)
        # self.playerRegionSurfaces[player.index] = pygame.transform.rotate(surface, (90*player.index))
    
    def drawDraftRegion(self, player):
        surface = self.draftRegionSurfaces[player.index]
        surface.fill(COLORS['BLACK'])
        rect = pygame.Rect(0, 0, DRAFT_WIDTH, DRAFT_HEIGHT)
        pygame.draw.rect(surface, player.color, rect, 2)
        # self.draftRegionSurfaces[player.index] = pygame.transform.rotate(surface, (90*player.index))

    def drawPieceInDraft(self, player, piece_index):
        self.drawDraftRegion(player)
        center = [DRAFT_WIDTH/2, DRAFT_HEIGHT/2]
        self.drawPiece(self.draftRegionSurfaces[player.index], player.pieces[piece_index], [center[0], center[1]], player.color)
    
    def drawPlayBoard(self):
        surface = self.playBoard
        surface.fill(COLORS['BLACK'])
        for x_ind in range(BOARD_NUM_x):
            for y_ind in range(BOARD_NUM_y):
                rect = pygame.Rect(BLOCK_SIZE*x_ind, BLOCK_SIZE*y_ind, BLOCK_SIZE, BLOCK_SIZE)
                blockownerindex = self.board.table4display[x_ind][y_ind]
                pygame.draw.rect(surface, COLORS['WHITE'], rect, 2)
                if blockownerindex > -1:
                    rect = pygame.Rect(BLOCK_SIZE*x_ind+1, BLOCK_SIZE*y_ind+1, BLOCK_SIZE-2, BLOCK_SIZE-2)
                    pygame.draw.rect(surface, self.getColorWithPlayerIndex(blockownerindex), rect, 0)
                else:
                    pass
        
    def getIndexOfBlockOnBoard(self, pos):
        x_ind = (pos[0] - BOARD_x) // BLOCK_SIZE
        y_ind = (pos[1] - BOARD_y) // BLOCK_SIZE
        x = math.floor(x_ind)
        y = math.floor(y_ind)
        x = max(0, min(x, BOARD_NUM_x-1))
        y = max(0, min(y, BOARD_NUM_y-1))
        return (x, y)
    
    def getCenterOfBlockOnBoard(self, indexes):
        x = BLOCK_SIZE*(indexes[0]+0.5)
        y = BLOCK_SIZE*(indexes[1]+0.5)
        return (x, y)
    
    def drawBlock(self, surface, center, color):
        rect = pygame.Rect(center[0]-BLOCK_SIZE/2+2, center[1]-BLOCK_SIZE/2+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
        pygame.draw.rect(surface, color, rect, 0)
    
    def drawSmallBlock(self, surface, center, color):
        rect = pygame.Rect(center[0]-SMALL_BLOCK_SIZE/2+2, center[1]-SMALL_BLOCK_SIZE/2+2, SMALL_BLOCK_SIZE-4, SMALL_BLOCK_SIZE-4)
        pygame.draw.rect(surface, color, rect, 0)
    
    def drawPiece(self, surface, piece, center, color):
        (dimx, dimy) = piece.current_shape()
        for x_ind in range(dimx):
            x = center[0]+BLOCK_SIZE*(x_ind-dimx/2+0.5)
            for y_ind in range(dimy):
                y = center[1]+BLOCK_SIZE*(y_ind-dimy/2+0.5)
                if piece.current_variant()[x_ind][y_ind] > 0:
                    self.drawBlock(surface, [x, y], color)
    
    def drawSmallPicece(self, surface, piece, center, color):
        (dimx, dimy) = piece.ini_shape()
        for x_ind in range(dimx):
            x = center[0]+SMALL_BLOCK_SIZE*(x_ind-dimx/2+0.5)
            for y_ind in range(dimy):
                y = center[1]+SMALL_BLOCK_SIZE*(y_ind-dimy/2+0.5)
                if piece.ini_variant()[x_ind][y_ind] > 0:
                    self.drawSmallBlock(surface, [x, y], color)
    
    def drawGuideBlock(self, player):
        surface = self.guideBlockSurfaces[player.index]
        surface.fill(player.color)
    
    def dealWithMouseLeftDown(self, pos):
        i = self.current_player_index
        player = self.players[i]
        if self.playerRegionRects[i].collidepoint(pos):
            # print("Player Region " + str(i) + " is selected.")
            self.selectPieceIntoDraft(pos, self.players[i])
        elif self.playBoardRect.collidepoint(pos):
            print("Play Board is selected : " + str(self.getIndexOfBlockOnBoard(pos)))
            indexes = self.getIndexOfBlockOnBoard(pos)
            if self.PlayerStatus == Blokus.STATUS_InDraft and self.board.validatePotentialPlacement(indexes, player, self.players[i].current_piece()):
                piece = self.players[i].current_piece()
                self.players[i].remove_piece_from_remaining(self.players[i].current_piece_index())
                self.board.updateTable(indexes, self.current_player_index, piece)
                piece.status = Piece.STATUS_InBoard
                self.board.resetTable4Display()
                self.drawPlayBoard()
                self.nextPlayer()
                self.PlayerStatus = Blokus.STATUS_InStock
        else:
            pass
    
    def dealWithMouseLeftUp(self, pos):
        pass

    def dealWithMouseMiddleDown(self, pos):
        i = self.current_player_index
        if self.draftRegionRects[i].collidepoint(pos):
            # print("Player Draft " + str(i) + " is selected.")
            self.rotatePieceInDraft(self.players[i], -1)

    def dealWithMouseMiddleUp(self, pos):
        i = self.current_player_index
        if self.draftRegionRects[i].collidepoint(pos):
            # print("Player Draft " + str(i) + " is selected.")
            self.rotatePieceInDraft(self.players[i], 1)
    
    def dealWithMouseMotion(self, pos):
        if self.playBoardRect.collidepoint(pos):
            indexes = self.getIndexOfBlockOnBoard(pos)
            if indexes != self.blockIndexesOnBoard:
                self.blockIndexesOnBoard = indexes
                #print("Mouse moved above Play Board : " + str(indexes))
                if self.PlayerStatus == Blokus.STATUS_InDraft:
                    print("Mouse moved above Play Board : " + str(indexes))
                    self.board.resetTable4Display()
                    piece = self.players[self.current_player_index].current_piece()
                    self.board.updateDisplayTable(indexes, self.current_player_index, piece)
                    self.drawPlayBoard()
                    #print("self.board.table4display is " + str(self.board.table4display))
        
        
    def dealWithMouseRightDown(self, pos):
        pass

    def dealWithMouseRightUp(self, pos):
        pass

    def selectPieceIntoDraft(self, pos, player):
        for i in range(21):
            if self.playerPiecesRects[player.index][i].collidepoint(pos):
               # redraw draft region
               if (player.pieces[i].status == Piece.STATUS_InStock):
                   # restore the previous piece
                   for j in range(21):
                       if j != i and player.pieces[j].status == Piece.STATUS_InDraft:
                           player.pieces[j].status = Piece.STATUS_InStock
                   # draw selected piece into draft region
                   player.pieces[i].status = Piece.STATUS_InDraft
                   self.drawPieceInDraft(player, i)
                   # redraw player region
                   self.drawPlayerRegion(player)
                   self.PlayerStatus = Blokus.STATUS_InDraft
                   print("Player " + str(player.index) + " selects the piece " + str(i) + " with variant " + str(player.pieces[i].curent_idx()) + " in Draft")
               break
    
    def rotatePieceInDraft(self, player, direction = 1):
        # get the piece in draft region
        piece = None
        piece_index = 255
        for i in range(21):
            if player.pieces[i].status == Piece.STATUS_InDraft:
                piece = player.pieces[i]
                piece_index = i
                break
        if piece is None:
            return
        if direction == 1:
            piece.next_variant()
        else:
            piece.previous_variant()
        self.drawPieceInDraft(player, piece_index)
        print("Player " + str(player.index) + " selects the piece " + str(piece_index) + " with variant " + str(piece.curent_idx()))
        
    def run(self):

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = tuple(i * self.scale for i in pos)
                if event.button == 1:
                    self.dealWithMouseLeftDown(pos)
                elif event.button == 2:
                    pass
                elif event.button == 3:
                    self.dealWithMouseRightDown(pos)
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = tuple(i * self.scale for i in pos)
                if event.button == 1:
                    self.dealWithMouseLeftUp(pos)
                elif event.button == 2:
                    pass
                elif event.button == 3:
                    self.dealWithMouseRightUp(pos)
                else:
                    pass
            elif event.type == pygame.MOUSEWHEEL:
                pos = pygame.mouse.get_pos()
                pos = tuple(i * self.scale for i in pos)
                if event.y > 0:
                    self.dealWithMouseMiddleDown(pos)
                elif event.y < 0:
                    self.dealWithMouseMiddleUp(pos)
                else:
                    pass
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                pos = tuple(i * self.scale for i in pos)
                self.dealWithMouseMotion(pos)

            else:
                pass
            
            self.updateGUI()
            pygame.display.update()
        
 
if __name__ == '__main__':
    bl = BlokusPyGame()
    bl.initGUI()
    bl.run()
    
