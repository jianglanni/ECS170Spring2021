# Lan Jiang
# ECS170
# HW2
# :)

import heapq

visited = []
frontier = []  # (f, g, state), a heap priority queue
prev = {}  # to save the route


# Find a state in frontier
def frontier_search(state_str):
    ret = -1
    for i in range(0, len(frontier)):
        if state_str == frontier[i]:
            ret = i
            break
    return ret


def rushhour(heu, state_mat):
    from_goal = rushhour_astar(heu, mat_to_str(state_mat))
    route = []
    while from_goal != "":
        route.append(from_goal)
        from_goal = prev[from_goal]
    for i in range(0, len(route))[::-1]:
        print_boi(str_to_mat(route[i]))
    print("Total moves:", len(route) - 1)
    print("Total states explored:", len(frontier) + len(visited))


# Main problem solver
def rushhour_astar(heu, state_str):
    if heu == 0:
        heapq.heappush(frontier, (h_block(state_str), 0, state_str))
    else:
        heapq.heappush(frontier, (0, 0, state_str))
    prev[state_str] = ""
    #  A* algorithm starts here
    while len(frontier):
        state_tuple = heapq.heappop(frontier)
        visited.append(state_tuple[2])
        next_steps = new_moves(state_tuple[2])
        for step in next_steps:
            if step in visited:
                continue
            if is_goal(step):
                prev[step] = state_tuple[2]
                return step
            cur_g = state_tuple[1] + 1 # new g value
            cur_f = cur_g
            if heu == 0:  # Given heuristic
                cur_f += h_block(state_tuple[2])
            else:  # My heuristic
                cur_f += 0
            if frontier_search(step) != -1:  # Detected this state in frontier already
                temp_loc = frontier_search(step)
                if cur_g < frontier[temp_loc][1]:  # Current g is smaller than existing g
                    frontier[temp_loc] = (cur_f, cur_g, step)  # renew the frontier
                    heapq.heapify(frontier)  # Keep the frontier in order
                    prev[step] = state_tuple[2]  # Route update
            else:
                prev[step] = state_tuple[2]  # Route
                heapq.heappush(frontier, (cur_f, cur_g, step))  # Update frontier
    print("Failed")
    return ""


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


def is_goal(state_str):
    return state_str[coord(2, 5)] == 'X'


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
    print("")


state2 = ["--B---","--B---","XXB---","--AA--","------","------"]
state3 = ["--A---","--ABBB","--XXC-","----C-","----D-","----D-"]
rushhour(0, state3)
