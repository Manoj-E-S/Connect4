
############################################################# IMPORTS ############################################################

import sys
import pygame
from pygame.locals import *
from tkinter import messagebox
import numpy as np
import math

##################################################################################################################################

######################################################## Global Variables ########################################################

# Connect 4 Grid
ROWS = 8
COLS = 9

# Pygame Screen
SCREEN_W = 1000
SCREEN_H = 1000

# Pygame Grid
GRID_R = ROWS+1
GRID_C = COLS
GRID_SIDE = SCREEN_H // GRID_R

# Colours
BACKGROUND = (0, 0, 0)
BOARD_COLOR = (0, 100, 200)
SLOT_COLOR = BACKGROUND
PLAYER_COLOR = ((150, 200, 255), (0, 255, 200))

# Mouse hover state
HOVER = False

##################################################################################################################################

############################################################ UTILITIES ###########################################################

def isValidLoc(board, row, col):
    return board[row][col] == 0

#_________________________________________________________________________________________________________________________________

def isWinningMove(board, player):
    
    # Horizontal Quads:
    for r in range(board.shape[0]-1, -1, -1):
        for c in range(0, board.shape[1] - 3):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Vertical Quads:
    for r in range(board.shape[0]-1, board.shape[0]-4, -1):
        for c in range(0, board.shape[1]):
            if board[r][c] == player and board[r-1][c] == player and board[r-2][c] == player and board[r-3][c] == player:
                return True

    # Principal Diagonal Quads:
    for r in range(board.shape[0]-4, -1, -1):
        for c in range(0, board.shape[1]-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    
    # Non-Principal Diagonal Quads:
    for r in range(board.shape[0]-1, board.shape[0]-4, -1):
        for c in range(0, board.shape[1]-3):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

    return False

#___________________________________________________________________________________________________________________________________

def insertToCol(board, column, player):
    
    for i in range(board.shape[0]):
        if i == board.shape[0] - 1 or board[i+1][column] != 0:
            if isValidLoc(board, i, column):
                board[i][column] = player
                break
            else:
                print("INVALID COLUMN")
                break

    return board

#___________________________________________________________________________________________________________________________________
#_____________________________________________________ GRAPHIC  UTILITIES __________________________________________________________

def winMessage(window, player):
    pygame.draw.rect(window, BACKGROUND, (0, 0, SCREEN_W, GRID_SIDE))
    font = pygame.font.SysFont("lato", GRID_SIDE - 30)
    label = font.render(f"Player {player+1} Wins!!!", 1, PLAYER_COLOR[player])
    window.blit(label, (GRID_SIDE//5, GRID_SIDE//6))
    pygame.display.update()

#___________________________________________________________________________________________________________________________________

def popupMessage(player):
    response = messagebox.askquestion("GAME OVER", f"Player {player+1} WON!\nDO you want to Play Again?")
    if response == "yes":
        return False
    return True

#___________________________________________________________________________________________________________________________________

def mouseHover(window, mousex, player):
    x = math.floor(mousex//GRID_SIDE) * GRID_SIDE
    centre = (x + GRID_SIDE//2, GRID_SIDE//2)
    pygame.draw.circle(window, PLAYER_COLOR[player], centre, GRID_SIDE//2 - 2)

#___________________________________________________________________________________________________________________________________

def drawSlots(window, board, mousex, player):
    for i in range(ROWS):
        for j in range(COLS):
            x = j*GRID_SIDE + (GRID_SIDE//2)
            y = i*GRID_SIDE + GRID_SIDE + (GRID_SIDE//2)
            centre = (x, y)
            if board[i][j] == 0:
                pygame.draw.circle(window, SLOT_COLOR, centre, (GRID_SIDE//2 - 2))
            elif board[i][j] == 1:
                pygame.draw.circle(window, PLAYER_COLOR[0], centre, (GRID_SIDE//2 - 2))
            else:
                pygame.draw.circle(window, PLAYER_COLOR[1], centre, (GRID_SIDE//2 - 2))
    
#____________________________________________________________________________________________________________________________________

def redrawBoard(window, board, mousex, player):
     global HOVER
     window.fill(BACKGROUND)
     pygame.draw.rect(window, BOARD_COLOR, (0, GRID_SIDE, SCREEN_W, (SCREEN_H - GRID_SIDE)))
     drawSlots(window, board, mousex, player)
     if HOVER:
         mouseHover(window, mousex, player)
         HOVER = False
     pygame.display.update()

#####################################################################################################################################

################################################################ GAME ###############################################################

def game():
    
    global HOVER
    board = np.zeros((ROWS, COLS), dtype=np.uint16)

    game_over = False
    player = 0

    # The Game
    pygame.init()
    
    window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Connect FOUR")
    
    clk = pygame.time.Clock()
    
    while not game_over:
        
        clk.tick(9)
        mousex = 0
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                game_over = True
            
            if event.type == MOUSEMOTION:
                mousex = event.pos[0]
                HOVER = True
            
            if event.type == MOUSEBUTTONUP:
                mousex = event.pos[0]
                col = math.floor(mousex // GRID_SIDE) + 1
                board = insertToCol(board, col-1, player+1)
                
                if isWinningMove(board, player+1):
                    redrawBoard(window, board, mousex, player)
                    winMessage(window, player)
                    game_over = popupMessage(player)
                    if not game_over:
                        board = np.zeros((ROWS, COLS), dtype=np.uint16)

                player = 1 if player == 0 else 0
        
        redrawBoard(window, board, mousex, player)
        

    pygame.display.quit()
    pygame.quit()
    sys.exit()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__':
    game()

##################################################################################################################################
