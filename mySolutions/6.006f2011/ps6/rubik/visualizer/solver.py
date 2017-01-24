import rubik

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    level = {start:0}
    parent = {start:None}
    i = 1
    frontier = [start]
    solution = []
    while end not in level:              # explore graph
#         print frontier
        next = []
        for u in frontier:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move,u)
                if v == end:
                	print 'found a solution'
                if v not in level:
#                     print 'currentPos = ',currentPos
                    level[v] = i
                    parent[v] = (u,move)
                    next.append(v)
        frontier = next
    newEnd = end
    for i in range(level[end]):
         solution.append(parent[end][1])
         newEnd = solution[-1]
    return solution

#     if start == end:
#     	return solution
