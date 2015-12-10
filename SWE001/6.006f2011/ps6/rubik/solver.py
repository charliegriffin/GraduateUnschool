import rubik

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    level = {start:0}
    backLevel = {end:0}
    parent = {start:None}
    backParent = {end:None}
    i = 1
    frontier = [start]
    solution = []
    backFrontier = [end]
    connected = False
    connections = []
    while (not connected) and (i <= 7):              # explore graph
        next = []
        for u in frontier:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move,u)
                if v not in level:
                    level[v] = i
                    parent[v] = (u,move)
                    next.append(v)
        frontier = next
        backNext = []
        for u in backFrontier:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move,u)
                if v not in backLevel:
                    backLevel[v] = i
                    backParent[v] = (u,rubik.perm_inverse(move))
                    backNext.append(v)
        backFrontier = backNext
        for config in level.keys():
            if config in backLevel:
                connected = True
                connections.append(config)
        i += 1
    if not connected:      # we have explored all options and found no solution
        return None
    minConn = findShortestPath(connections,level,backLevel)
    # join the partial solutions
    newCenter = minConn
    for i in range(level[minConn]):
        (pos,move) = parent[newCenter]
        solution.append(move)
        newCenter = pos
    solution.reverse()
    newCenter = minConn
    for i in range(backLevel[minConn]):
        (pos,move) = backParent[newCenter]
        solution.append(move)
        newCenter = pos
    return solution

def findShortestPath(connections,level,backLevel):
    minDistance = 15 # this serves as an infinity
    for conn in connections:
        distance = level[conn] + backLevel[conn]
        if distance < minDistance:
            minConn = conn
            minDistance = distance
    return minConn