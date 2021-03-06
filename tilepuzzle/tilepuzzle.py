# Lan Jiang
# ECS170
# HW1
# Please give the program enough time (like 60 seconds) to run, thanks!
# Feel free to modify the depth_list on Line 10


# Try to find an answer quickly by giving different depth limits to the searches
def tilepuzzle(initial, goal):
    depth_list = [5, 15, 30] # Three different depth limits
    for depth_limit in depth_list:
        ret = statesearch(initial, goal, [], 0, depth_limit)[::-1]
        if ret:
            return ret
        visited.clear()

    print("This puzzle cannot be solved in limited steps.")
    return []


def statesearch(current, goal, path, depth, limit):
    if current == goal:
        path.append(current)
        return path

    # Add current state to the visited state list
    current_visit = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
    for i in range(0, 3):
        for j in range(0, 3):
            current_visit[i][j] = current[i][j]
    visited.append(current_visit)

    # generate a list that contains the next possible moves from the current state
    moves = newStatus(current)

    # Dead end
    if moves == []:
        visited.pop(-1)
        return []

    # Too deep, escape!
    if depth > limit:
        visited.pop(-1)
        return []

    # Peek ahead
    for nextMove in moves:
        if nextMove == goal:
            path.append(goal)
            path.append(current)
            return path

    # Recursive, deeper search (DFS)
    for nextMove in moves:
        temp = statesearch(nextMove, goal, path, depth+1, limit)
        if temp != [] and temp[0] == goal:
            path.append(current)
            return path

    # All "nextmoves" go to dead ends
    visited.pop(-1)
    return []


visited = []


# To check if a state has been visited
def isVisited(status):
    for ins in visited:
        if ins == status:
            return True
    return False


# This function generates the new states based on the current state
def newStatus(current):
    ret = []
    col = -1
    row = -1
    # Find where the hole is
    for i in range(0, 3):
        for j in range(0, 3):
            if current[i][j] == 0:
                row = i
                col = j
    if row > 0:
        temp = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        for i in range(0, 3):
            for j in range(0, 3):
                temp[i][j] = current[i][j]
        temp[row][col], temp[row - 1][col] = temp[row - 1][col], temp[row][col]
        if not isVisited(temp):
            ret.append(temp)

    if row < 2:
        temp = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        for i in range(0, 3):
            for j in range(0, 3):
                temp[i][j] = current[i][j]
        temp[row][col], temp[row + 1][col] = temp[row + 1][col], temp[row][col]
        if not isVisited(temp):
            ret.append(temp)

    if col > 0:
        temp = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        for i in range(0, 3):
            for j in range(0, 3):
                temp[i][j] = current[i][j]
        temp[row][col], temp[row][col - 1] = temp[row][col - 1], temp[row][col]
        if not isVisited(temp):
            ret.append(temp)

    if col < 2:
        temp = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
        for i in range(0, 3):
            for j in range(0, 3):
                temp[i][j] = current[i][j]
        temp[row][col], temp[row][col + 1] = temp[row][col + 1], temp[row][col]
        if not isVisited(temp):
            ret.append(temp)

    return ret


# My own test case
# start = [[0,8,7],[6,5,4],[3,2,1]]
# end = [[1,2,3],[4,5,6],[7,8,0]]
# answer = tilepuzzle(start, end)
# for e in answer:
#     print(e)
# print(len(answer))
