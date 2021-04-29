# Lan Jiang
# ECS170
# HW2
# :)

import heapq

visited = []
frontier = []  # (f, g, state), a heap priority queue
prev = {}  # to save the route


# Blocking heuristic
def h_block(state_str):
    if state_str[coord(2, 5)] == 'X':
        return 0  # goal state reached
    mat = str_to_mat(state_str)
    vehicle_block = 0
    for i in range(0, 6)[::-1]:
        if mat[2][i] == 'X':
            return vehicle_block + 1  # X car detected, return the value
        elif mat[2][i] != '-':
            vehicle_block += 1  # vehicle detected
    assert 0  # No X car found, escape


# My heuristic. H = blocking + distance from X to exit
def m_block(state_str):
    if state_str[coord(2, 5)] == 'X':
        return 0  # goal state reached
    mat = str_to_mat(state_str)
    block_count = 0
    for i in range(0, 6)[::-1]:  # go through row where the X car at
        if mat[2][i] == 'X':
            return block_count + 1  # X car detected, return the value
        elif mat[2][i] != '-':
            block_count += 2  # vehicle detected + 1, dist + 1
        else:
            block_count += 1  # An empty space, dist + 1
    assert 0  # No X car found, escape


# Called by users
def rushhour(heu, state_mat):
    from_goal = rushhour_astar(heu, mat_to_str(state_mat))  # This returns the goal state that helps reconstruction
    route = []
    while from_goal != "":  # Reconstruct route
        route.append(from_goal)
        from_goal = prev[from_goal]
    for i in range(0, len(route))[::-1]:
        print_boi(str_to_mat(route[i]))
    print("Total moves:", len(route) - 1)  # Exclude the start state itself.
    print("Total states explored:", len(frontier) + len(visited))


# Main problem solver
def rushhour_astar(heu, state_str):
    if heu == 0:
        heapq.heappush(frontier, (h_block(state_str), 0, state_str))
    else:
        heapq.heappush(frontier, (m_block(state_str), 0, state_str))
    prev[state_str] = ""
    #  A* algorithm starts here
    while len(frontier):
        state_tuple = heapq.heappop(frontier)  # Getting the state with smallest f
        if is_goal(state_tuple[2]):
            return state_tuple[2]  # Goal detected
        visited.append(state_tuple)  # Mark as visited
        next_steps = new_moves(state_tuple[2])
        for step in next_steps:
            cur_g = state_tuple[1] + 1 # new g value
            cur_f = cur_g
            if heu == 0:  # Given heuristic
                cur_f += h_block(state_tuple[2])
            else:  # My heuristic
                cur_f += m_block(state_tuple[2])
            temp_loc = visited_search(step)
            if temp_loc != -1:  # Found this state in the closed set
                if cur_g >= visited[temp_loc][1]:
                    continue
                else:  # If we get a smaller g value than the one in the closed set
                    visited.pop(temp_loc)
                    prev[step] = state_tuple[2]  # Update route
                    heapq.heappush(frontier, (cur_f, cur_g, step))  # Put it back into the frontier
            temp_loc = frontier_search(step)  # Check if this state is already in frontier
            if temp_loc != -1:
                if cur_g < frontier[temp_loc][1]:  # Current g is smaller than existing g
                    frontier[temp_loc] = (cur_f, cur_g, step)  # renew the frontier
                    heapq.heapify(frontier)  # Sort the frontier
                    prev[step] = state_tuple[2]  # Route update
            else:
                prev[step] = state_tuple[2]  # Route
                heapq.heappush(frontier, (cur_f, cur_g, step))  # Update frontier
    print("Failed")
    return ""  # Failed


# Find a state in frontier
def frontier_search(state_str):
    ret = -1
    for i in range(0, len(frontier)):
        if state_str == frontier[i][2]:
            ret = i
            break
    return ret


# Find a state in the closed list
def visited_search(state_str):
    ret = -1
    for i in range(0, len(visited)):
        if state_str == visited[i][2]:
            ret = i
            break
    return ret


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


# Coordinate converter
def coord(x, y):
    return 6 * x + y


# Goal check
def is_goal(state_str):
    return state_str[coord(2, 5)] == 'X'


# New states generator
def new_moves(state_str):
    ret = []
    for i in range(0, 6):
        for j in range(0, 6):
            temp = car_right(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_down(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_left(state_str, i, j)
            if temp:
                ret.append(temp)
            temp = car_up(state_str, i, j)
            if temp:
                ret.append(temp)
    return tuple(ret)


# Vehicle goes left
def car_left(state_str, i, j):
    is_truck = False
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
            is_truck = True
    mat[i][j-1] = mat[i][j]
    if is_truck:
        mat[i][j+2] = '-'
    else:
        mat[i][j+1] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


# Vehicle goes right
def car_right(state_str, i, j):
    is_truck = False
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
            is_truck = True
    mat[i][j+1] = mat[i][j]
    if is_truck:
        mat[i][j-2] = '-'
    else:
        mat[i][j-1] = '-'
    mat[i] = ''.join(mat[i])
    ret = mat_to_str(mat)
    return ret


# Vehicle goes up
def car_up(state_str, i, j):
    is_truck = False
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 0 or i == 5:
        return []
    if mat[i][j] != mat[i+1][j] or mat[i-1][j] != '-':
        return []
    if 0 < i < 4:  # it is a truck
        if mat[i][j] == mat[i+2][j]:
            is_truck = True
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i-1][j] = mat[i][j]
    if is_truck:
        mat[i+2][j] = '-'
    else:
        mat[i+1][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


# Vehicle goes down
def car_down(state_str, i, j):
    is_truck = False
    mat = str_to_mat(state_str)
    if mat[i][j] == '-':
        return []
    if i == 0 or i == 5:
        return []
    if mat[i][j] != mat[i-1][j] or mat[i+1][j] != '-':
        return []
    if 1 < i < 5:  # it is a truck
        if mat[i][j] == mat[i-2][j]:
            is_truck = True
    for k in range(0, 6):
        mat[k] = list(mat[k])
    mat[i+1][j] = mat[i][j]
    if is_truck:
        mat[i-2][j] = '-'
    else:
        mat[i-1][j] = '-'
    for k in range(0, 6):
        mat[k] = ''.join(mat[k])
    ret = mat_to_str(mat)
    return ret


# Matrix printer
def print_boi(mat):
    for i in range(0, 6):
        print(mat[i])
    print("")


# My test cases
state1 = ["--AABB","--CDEF","XXCDEF","--GGHH","------","------"]
state2 = ["--B---","--B---","XXB---","--AA--","------","------"]
state3 = ["--A---","--ABBB","--XXC-","----C-","----D-","----D-"]
state4 = ["---A--","---A--","XX-A--","BCCC--","B-----","B-----"]
state5 = ["GBB-L-","GHI-LM","GHIXXM","CCCK-M","--JKDD","EEJFF-"]
state6 = ["-AA---", "-BBB-C", "XX---C", "---D-C", "---D--", "------"]
rushhour(0, state3)
