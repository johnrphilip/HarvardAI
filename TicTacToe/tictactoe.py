"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Does this by counting the total of x or O
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return O if x_count > o_count else X
    

# takes board input
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    runs through i,j up and down to see if there are any empties in the 2d board
    """
    return{(i,j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid move")
    
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board
    

def winner(board):
    # Returns the winner of the game, if there is one.
    # starts with rows
    for i in range(3):
        if board [i][0] == board[i][1] == board [i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        #then the columns
        if board [0][i] == board[1][i] == board [2][i] and board[0][i] is not EMPTY:
            return board[0][i]
        
    # check the two diagonals
    if board [0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board [2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    #if no winner
    return None
        
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):

    # determines who's turn it is and calls their strategy up
    if player(board) == X:
        value, move = max_x_player(board)
    else:
        value, move = min_o_player(board)
    return move

def max_x_player(board):
    #first check if the game is over
    if terminal(board):
        return utility(board), None

    # set the value used to determine a best move
    v = float("-inf")
    best_move = None  # creating empty best move variable
    # set the loop and call the action function for each possible move with empty spaces
    for action in actions(board):
        # calculate the minimum value that the opponent can get after the move is made. '_' ignores the actual move
        min_val, _ = min_o_player(result(board, action))
        # compare the opponents min_value to the v here for X. if v makes the number bigger then v then update the best move
        if min_val > v:
            v = min_val   # update the new value
            best_move = action #store this action
    return v, best_move



def min_o_player(board):
    #first check if the game is over
    if terminal(board):
        return utility(board), None

    # set the value used to determine a best move
    v = float("inf")
    best_move = None  # creating empty best move variable
    # set the loop and call the action function for each possible move with empty spaces
    for action in actions(board):
        # calculate the minimum value that the opponent can get after the move is made. '_' ignores the actual move
        max_val, _ = max_x_player(result(board, action))
        # compare the opponents min_value to the v here for X. if v makes the number bigger then v then update the best move
        if max_val < v:
            v = max_val   # update the new value
            best_move = action #store this action
    return v, best_move