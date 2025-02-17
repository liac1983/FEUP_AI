from collections import deque

def is_valid(state):
    """ Check if the state is valid (no more cannibals than missionaries on any side). """
    m_left, c_left, _ = state
    m_right, c_right = 3 - m_left, 3 - c_left
    
    if (m_left < c_left and m_left > 0) or (m_right < c_right and m_right > 0):
        return False
    return True

def bfs_search():
    """ Solve the problem using Breadth-First Search (BFS). """
    initial_state = (3, 3, 1)
    goal_state = (0, 0, 0)
    queue = deque([(initial_state, [])])
    visited = set()
    
    while queue:
        state, path = queue.popleft()
        
        if state == goal_state:
            return path + [state]
        
        if state in visited:
            continue
        visited.add(state)
        
        for move in [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]:
            m_move, c_move = move
            m, c, boat = state
            
            if boat == 1:
                new_state = (m - m_move, c - c_move, 0)
            else:
                new_state = (m + m_move, c + c_move, 1)
            
            if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state):
                queue.append((new_state, path + [state]))
    return None

def dfs_limited(state, path, depth, max_depth, visited):
    """ Depth-First Search (DFS) with depth limit. """
    if state == (0, 0, 0):
        return path + [state]
    
    if depth >= max_depth:
        return None
    
    visited.add(state)
    
    for move in [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]:
        m_move, c_move = move
        m, c, boat = state
        
        if boat == 1:
            new_state = (m - m_move, c - c_move, 0)
        else:
            new_state = (m + m_move, c + c_move, 1)
        
        if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state) and new_state not in visited:
            result = dfs_limited(new_state, path + [state], depth + 1, max_depth, visited)
            if result:
                return result
    return None

def iterative_deepening():
    """ Iterative Deepening Depth-First Search (IDDFS). """
    max_depth = 20
    for depth in range(max_depth + 1):
        visited = set()
        result = dfs_limited((3, 3, 1), [], 0, depth, visited)
        if result:
            return result
    return None

# Run BFS solution
bfs_solution = bfs_search()
print("BFS Solution:")
if bfs_solution:
    for step in bfs_solution:
        print(step)
else:
    print("No solution found.")

# Run DFS solution with depth limit
dfs_solution = dfs_limited((3, 3, 1), [], 0, 10, set())
print("\nDFS Limited Depth Solution:")
if dfs_solution:
    for step in dfs_solution:
        print(step)
else:
    print("No solution found.")

# Run IDDFS solution
iddfs_solution = iterative_deepening()
print("\nIterative Deepening DFS Solution:")
if iddfs_solution:
    for step in iddfs_solution:
        print(step)
else:
    print("No solution found.")
