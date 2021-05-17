# Lan Jiang
# ECS170
# HW3
# =w=

# Interface for testing, and evaluate the board for the first level, return [] if the given state is an endgame
# At the end, all the children whose depths are 1 are kept in moves, in tuples (minimax_value, state)
def hexapawn(state_mat, size, turn, depth):
    state_str = mat_to_str(state_mat)
    if abs(board_eval(state_str, size)) == 99:  # Endgame case 1
        return []
    moves = new_moves(state_str, size, turn)  # Get the new moves
    if len(moves) == 0:  # Endgame case 2
        return []
    moves = list(moves)
    if turn == 'b':
        for i in range(0, len(moves)):
            moves[i] = recur_pawn_game(moves[i], size, 'w', depth-1), moves[i]  # Ask for minimax board values
    elif turn == 'w':
        for i in range(0, len(moves)):
            moves[i] = recur_pawn_game(moves[i], size, 'b', depth-1), moves[i]  # Ask for minimax board values
    moves.sort(reverse=(turn == 'b'))  # Sort all moves from smallest to biggest if white, opposite if black
    return str_to_mat(moves[0][1], size)  # Return the board with the smallest (white)/ biggest (black) value


# The minimax evaluator, taking a state, size, turn, and depth, search, returns the board value based on its children
# Search down the game tree recursively
# The function also determines if a player loses due to not being able to make any moves
def recur_pawn_game(state_str, size, turn, depth):
    board_value = board_eval(state_str, size)
    if depth == 0 or abs(board_value) == 99:  # Hit the bottom or win
        return board_value
    moves = new_moves(state_str, size, turn)
    if len(moves) == 0:  # No more moves for the current player, lose
        if turn == 'b':
            return -99
        if turn == 'w':
            return 99
    moves = list(moves)
    # Minimax starts here!
    if turn == 'b':  # It's black's turn to move
        for i in range(0, len(moves)):
            moves[i] = recur_pawn_game(moves[i], size, 'w', depth-1)
            if moves[i] == 99:  # In case it just wins.
                return moves[i]  # Immediately jump out due to the winning
        moves.sort(reverse=True)
    if turn == 'w':  # It's white's turn to move
        for i in range(0, len(moves)):
            moves[i] = recur_pawn_game(moves[i], size, 'b', depth-1)
            if moves[i] == -99:  # Win!
                return moves[i]  # Immediately jump out
        moves.sort(reverse=False)
    return moves[0]  # Give the result (board value)


# Static board evaluator. 99 for black win, -99 for white win, black-white otherwise, based on the board only
# For optimization purpose, this function do not return +/-99 when there are no moves for a player
def board_eval(state_str, size):
    state_mat = str_to_mat(state_str, size)
    black_pawn = 0
    white_pawn = 0
    # Scan the board, count the pawns
    for i in range(0, size):
        for j in range(0, size):
            if i == 0 and state_mat[i][j] == 'b':
                return 99  # hit the end
            if i == size - 1 and state_mat[i][j] == 'w':
                return -99  # hit the end
            if state_mat[i][j] == 'b':
                black_pawn += 1
            elif state_mat[i][j] == 'w':
                white_pawn += 1
    if black_pawn == 0:  # All opponents killed
        return -99
    if white_pawn == 0:
        return 99
    return black_pawn - white_pawn  # default


# The following functions generate new moves, taking the current state, size, and turn
def new_moves(state_str, size, turn):
    ret = []
    for i in range(0, size):  # For each space on the board, check if there are any possible moves for the pawn on it
        for j in range(0, size):
            if turn == 'w':
                ret = ret + w_move(state_str, size, i, j)
                ret = ret + w_kill(state_str, size, i, j)
            if turn == 'b':
                ret = ret + b_move(state_str, size, i, j)
                ret = ret + b_kill(state_str, size, i, j)
    return tuple(ret)  # Return a tuple that contains all possible moves from the given state


# Convert a state from a matrix to a string
def mat_to_str(state_mat):
    ret = ""
    for i in range(0, len(state_mat)):
        ret = ret + state_mat[i]
    return ret


# Convert a state from a string to a matrix
def str_to_mat(state_str, size):
    ret = []
    if len(state_str) != size*size:
        assert 0  # Wrong arguments
    for i in range(0, size*size)[::size]:
        ret.append(state_str[i:i+size])
    return ret


# A white pawn on (i, j) moves forward
def w_move(state_str, size, i, j):
    state_mat = str_to_mat(state_str, size)
    if i >= size - 1 or j >= size:
        return []  # Already hit the bottom or illegal
    if state_mat[i][j] != 'w' or state_mat[i+1][j] != '-':
        return []  # It is not a white pawn or it is blocked
    state_mat[i] = list(state_mat[i])
    state_mat[i+1] = list(state_mat[i+1])
    state_mat[i][j] = '-'
    state_mat[i+1][j] = 'w'
    state_mat[i] = ''.join(state_mat[i])
    state_mat[i+1] = ''.join(state_mat[i+1])  # A bunch of manipulations on the state, same for following functions
    return [mat_to_str(state_mat)]


# A white pawn on (i, j) kills
def w_kill(state_str, size, i, j):
    ret = []
    state_mat = str_to_mat(state_str, size)
    if i >= size - 1 or j >= size:
        return []  # Already hit the bottom or illegal
    if state_mat[i][j] != 'w':
        return []  # It is not a white pawn
    if j > 0:  # kill the left one
        if state_mat[i+1][j-1] == 'b':
            state_mat[i] = list(state_mat[i])
            state_mat[i+1] = list(state_mat[i+1])
            state_mat[i][j] = '-'
            state_mat[i+1][j-1] = 'w'
            state_mat[i] = ''.join(state_mat[i])
            state_mat[i+1] = ''.join(state_mat[i+1])
            ret.append(mat_to_str(state_mat))
    state_mat = str_to_mat(state_str, size)  # Reset the board from the previous move
    if j < size - 1:  # kill the right one
        if state_mat[i+1][j+1] == 'b':
            state_mat[i] = list(state_mat[i])
            state_mat[i+1] = list(state_mat[i+1])
            state_mat[i][j] = '-'
            state_mat[i+1][j+1] = 'w'
            state_mat[i] = ''.join(state_mat[i])
            state_mat[i+1] = ''.join(state_mat[i+1])
            ret.append(mat_to_str(state_mat))
    return ret  # Return a list that contains all next moves


# A black pawn on (i, j) moves forward
def b_move(state_str, size, i, j):
    state_mat = str_to_mat(state_str, size)
    if i <= 0 or j >= size:
        return []  # Already hit the bottom or illegal
    if state_mat[i][j] != 'b' or state_mat[i-1][j] != '-':
        return []  # It is not a black pawn or it is blocked
    state_mat[i] = list(state_mat[i])
    state_mat[i-1] = list(state_mat[i-1])
    state_mat[i][j] = '-'
    state_mat[i-1][j] = 'b'
    state_mat[i] = ''.join(state_mat[i])
    state_mat[i-1] = ''.join(state_mat[i-1])
    return [mat_to_str(state_mat)]


# A black pawn on (i, j) kills
def b_kill(state_str, size, i, j):
    ret = []
    state_mat = str_to_mat(state_str, size)
    if i <= 0 or j >= size:
        return []  # Already hit the bottom or illegal
    if state_mat[i][j] != 'b':
        return []  # It is not a black pawn
    if j > 0:  # Kill the left one
        if state_mat[i-1][j-1] == 'w':
            state_mat[i] = list(state_mat[i])
            state_mat[i-1] = list(state_mat[i-1])
            state_mat[i][j] = '-'
            state_mat[i-1][j-1] = 'b'
            state_mat[i] = ''.join(state_mat[i])
            state_mat[i-1] = ''.join(state_mat[i-1])
            ret.append(mat_to_str(state_mat))
    state_mat = str_to_mat(state_str, size)  # Reset the board from the previous move
    if j < size - 1:  # Kill the right one
        if state_mat[i-1][j+1] == 'w':
            state_mat[i] = list(state_mat[i])
            state_mat[i-1] = list(state_mat[i-1])
            state_mat[i][j] = '-'
            state_mat[i-1][j+1] = 'b'
            state_mat[i] = ''.join(state_mat[i])
            state_mat[i-1] = ''.join(state_mat[i-1])
            ret.append(mat_to_str(state_mat))
    return ret


# Properly print the board for debug, taking a string (state) and the size
def print_boi(state_str, size):
    mat = str_to_mat(state_str, size)
    for i in range(0, size):
        print(mat[i])
    print("")


# My test cases
# state1 = ["-w-w", "w-w-", "-b--", "b-bb"]
# state2 = ["-ww", "w--", "bbb"]
# state3 = ["www", "---", "bbb"]
# state4 = ["wwww", "----", "----", "bbbb"]
# print(hexapawn(state2, 3, 'b', 2))  # This one is the one on the slide
# print(hexapawn(state4, 4, 'w', 15))  # This one proves that the first mover on 4*4 100% wins
