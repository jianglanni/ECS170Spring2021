# matrix (list) to string
def mat_to_str(lst):
    ret = ""
    for row in lst:
        ret = ret + row
    return ret


# string to matrix
def str_to_mat(rows):
    ret = []
    for i in range(0, 31)[::6]:
        ret.append(rows[i:i+6])
    return ret


# Quick, direct access to string
def coord(x, y):
    return 6 * x + y


# Given heuristic
def h_block(state_str):
    if state_str[coord(2, 5)] == 'X':
        return 0  # goal state reached
    mat = str_to_mat(state_str)
    vehicle_block = 0
    for i in range(0, 6)[::-1]:
        if mat[2][i] == 'X':
            return vehicle_block + 1  # X car detected, return the value
        elif mat[2][i] != '-':
            vehicle_block = vehicle_block + 1 # vehicle detected
    assert 0  # No X car found


# New states generator
def new_moves(state_str):
    ret = []
    for i in range(0, 6):
        for j in range(0, 6):
            temp = car_left(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_right(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_up(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_down(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = truck_left(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = truck_right(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = truck_up(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = truck_down(state_str, i, j)
            if temp:
                ret.append(temp)
    return tuple(ret)


def car_left(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    mat[i] = list(mat[i])
    if j == 5 or j == 0:
        return []
    if mat[i][j-1] != '-' or mat[i][j] != mat[i][j+1]:
        return []
    if 0 < j < 4:  # It is a truck, not a car
        if mat[i][j] == mat[i][j+2]:
            return []
    mat[i][j-1] = mat[i][j]
    mat[i][j+1] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


def car_right(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    mat[i] = list(mat[i])
    if j == 5 or j == 0:
        return []
    if mat[i][j] != mat[i][j-1] or mat[i][j+1] != '-':
        return []
    if 1 < j < 5:
        if mat[i][j] == mat[i][j-2]:  # Truck detected
            return []
    mat[i][j+1] = mat[i][j]
    mat[i][j-1] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


def car_up(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 0 or i == 5:
        return []
    if mat[i][j] != mat[i+1][j] or mat[i-1][j] != '-':
        return []
    if 0 < i < 4:  # it is a truck
        if mat[i][j] == mat[i+2][j]:
            return []
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i-1][j] = mat[i][j]
    mat[i+1][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


def car_down(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 0 or i == 5:
        return []
    if mat[i][j] != mat[i-1][j] or mat[i+1][j] != '-':
        return []
    if 1 < i < 5:  # it is a truck
        if mat[i][j] == mat[i-2][j]:
            return []
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i+1][j] = mat[i][j]
    mat[i-1][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


def truck_left(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    mat[i] = list(mat[i])
    if j == 0 or j > 3:
        return []
    if not (mat[i][j] == mat[i][j+1] and mat[i][j] == mat[i][j+2]) or mat[i][j-1] != '-':
        return []
    mat[i][j-1] = mat[i][j]
    mat[i][j+2] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


def truck_right(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    mat[i] = list(mat[i])
    if j == 5 or j < 2:
        return []
    if not (mat[i][j] == mat[i][j-1] and mat[i][j] == mat[i][j-2]) or mat[i][j+1] != '-':
        return []
    mat[i][j+1] = mat[i][j]
    mat[i][j-2] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


def truck_up(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 0 or i > 3:
        return []
    if not (mat[i][j] == mat[i+1][j] and mat[i][j] == mat[i+2][j]) or mat[i-1][j] != '-':
        return []
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i-1][j] = mat[i][j]
    mat[i+2][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


def truck_down(state_str, i, j):
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 5 or i < 2:
        return []
    if not (mat[i][j] == mat[i-1][j] and mat[i][j] == mat[i-2][j]) or mat[i+1][j] != '-':
        return []
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i+1][j] = mat[i][j]
    mat[i-2][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


# Matrix printer
def print_boi(mat):
    for i in range(0, 6):
        print(mat[i])
    print('\n')


state = ["-BBB--","----CD","XX--CD","--AA-D","------","------"]
print_boi(state)
for i in new_moves(mat_to_str(state)):
    print_boi(str_to_mat(i))
print(h_block(mat_to_str(state)))
