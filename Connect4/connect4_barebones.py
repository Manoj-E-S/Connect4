import numpy as np


def isValidLoc(board, row, col):
    return board[row][col] == 0


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



def game():
    
    board = np.zeros((6, 7), dtype=np.uint16)

    game_over = False
    player = 1

    while not game_over:
        print(f"\n\n{board}")
        print("\n  1 2 3 4 5 6 7")
    
        col = int(input(f"\nPlayer {player}, enter column to insert into: "))
    
        board = insertToCol(board, col-1, player)
        
        if isWinningMove(board, player):
            print(f"\n\n{board}")
            print(f"\nPlayer {player} Wins!!\n")
            game_over = True

        player = 2 if player == 1 else 1



if __name__ == '__main__':
    game()
