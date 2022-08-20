"""
Tic Tac Toe Player
"""
import copy
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
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count = x_count + 1
            elif cell == O:
                o_count = o_count + 1
    if x_count + o_count == 9:
        return None
    elif x_count > o_count:
        return O
    elif x_count == o_count:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    if len(possible_moves) == 0:
        return None
    else:
        return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = initial_state()
    for i in range(0, 3):
        for j in range(0, 3):
            new_board[i][j] = copy.deepcopy(board[i][j])

    if new_board[action[0]][action[1]] != EMPTY:
        raise Exception
    else:
        new_board[action[0]][action[1]] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0, 3):
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X
        elif board[0][i] == X and board[1][i] == X and board[2][i] == X:
            return X
        elif board[i][0] == O and board[i][1] == O and board[i][2] == O:
            return O
        elif board[0][i] == O and board[1][i] == O and board[2][i] == O:
            return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    elif board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or player(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) is True:
        winner_symbol = winner(board)
        if winner_symbol == X:
            return 1
        elif winner_symbol == O:
            return -1
        elif winner_symbol is None:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        optimal = (-10, None)
        for action in actions(board):
            utility_value = min_value(result(board, action), optimal[0])
            if utility_value > optimal[0]:
                optimal = (utility_value, action)

    else:
        optimal = (10, None)
        for action in actions(board):
            utility_value = max_value(result(board, action), optimal[0])
            if utility_value < optimal[0]:
                optimal = (utility_value, action)

    return optimal[1]


def max_value(board, predecessor_v):
    if terminal(board):
        return utility(board)

    v = -10
    for action in actions(board):
        v = max(v, min_value(result(board, action), v))
        if v > predecessor_v:
            break
    return v


def min_value(board, predecessor_v):
    if terminal(board):
        return utility(board)

    v = 10
    for action in actions(board):
        v = min(v, max_value(result(board, action), v))
        if v < predecessor_v:
            break
    return v
