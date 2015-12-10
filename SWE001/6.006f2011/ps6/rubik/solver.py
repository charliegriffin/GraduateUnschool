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
    while end not in level:              # explore graph
#         print frontier
        next = []
        for u in frontier:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move,u)
                if v == end:
                	print 'found a solution\t length =',i
                if v not in level:
#                     print 'currentPos = ',currentPos
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
                    backParent[u] = (v,rubik.perm_inverse(move))
                    backNext.append(v)
        backFrontier = backNext
        i += 1
    newEnd = end
    for i in range(level[end]):
         (pos,move) = parent[newEnd]
         solution.append(move)
         newEnd = pos
    solution.reverse()# = reversed(solution)
    backSol = []
    newEnd = end
    for i in range(backLevel[start]):
        (pos,move) = parent[newEnd]
        backSol.append(move)
        newEnd = pos
    backSol.reverse()
    return solution

#     if start == end:
#     	return solution
