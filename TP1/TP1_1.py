from collections import deque

def bfs_bucket_problem(c1, c2, target):
    """
    Solves the Two Buckets Problem using Breadth-First Search (BFS)
    :param c1: Capacity of Bucket 1
    :param c2: Capacity of Bucket 2
    :param target: Goal amount of water in Bucket 1
    :return: List of steps leading to the goal state or None if no solution exists
    """
    queue = deque([((0, 0), [])])
    visited = set()
    
    while queue:
        (x, y), path = queue.popleft()
        
        if x == target:
            return path + [(x, y)]
        
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        next_states = [
            ((c1, y), "Fill Bucket 1"),
            ((x, c2), "Fill Bucket 2"),
            ((0, y), "Empty Bucket 1"),
            ((x, 0), "Empty Bucket 2"),
            ((max(0, x - (c2 - y)), min(c2, x + y)), "Pour Bucket 1 -> Bucket 2"),
            ((min(c1, x + y), max(0, y - (c1 - x))), "Pour Bucket 2 -> Bucket 1")
        ]
        
        for (new_state, action) in next_states:
            if new_state not in visited:
                queue.append((new_state, path + [(x, y, action)]))
    
    return None

def dfs_limited(state, path, depth, max_depth, visited, c1, c2, target):
    x, y = state
    
    if x == target:
        return path + [(x, y)]
    
    if depth >= max_depth:
        return None
    
    visited.add(state)
    
    next_states = [
        ((c1, y), "Fill Bucket 1"),
        ((x, c2), "Fill Bucket 2"),
        ((0, y), "Empty Bucket 1"),
        ((x, 0), "Empty Bucket 2"),
        ((max(0, x - (c2 - y)), min(c2, x + y)), "Pour Bucket 1 -> Bucket 2"),
        ((min(c1, x + y), max(0, y - (c1 - x))), "Pour Bucket 2 -> Bucket 1")
    ]
    
    for (new_state, action) in next_states:
        if new_state not in visited:
            result = dfs_limited(new_state, path + [(x, y, action)], depth + 1, max_depth, visited, c1, c2, target)
            if result:
                return result
    
    return None

def iterative_deepening(c1, c2, target, max_depth):
    for depth in range(max_depth + 1):
        visited = set()
        result = dfs_limited((0, 0), [], 0, depth, visited, c1, c2, target)
        if result:
            return result
    return None

c1, c2, target = 4, 3, 2
max_depth = 10

solution_bfs = bfs_bucket_problem(c1, c2, target)
solution_dfs = dfs_limited((0, 0), [], 0, max_depth, set(), c1, c2, target)
solution_iddfs = iterative_deepening(c1, c2, target, max_depth)

if solution_bfs:
    print("BFS Solution path:")
    for step in solution_bfs:
        print(step)
else:
    print("No BFS solution found.")

if solution_dfs:
    print("DFS Solution path:")
    for step in solution_dfs:
        print(step)
else:
    print("No DFS solution found.")

if solution_iddfs:
    print("Iterative Deepening DFS Solution path:")
    for step in solution_iddfs:
        print(step)
else:
    print("No Iterative Deepening DFS solution found.")
