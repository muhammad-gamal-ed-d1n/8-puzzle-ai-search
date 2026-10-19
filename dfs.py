import sys
import time

sys.setrecursionlimit(362880 // 2)

metrics = {"nodes_expanded": 0, "start_time": 0}

def search(initial, goal):
    metrics["nodes_expanded"] = 0
    metrics["start_time"] = time.perf_counter()
    
    parent_map = {hash_state(initial): None}
    state_map = {hash_state(initial): initial}
    
    found, end_hash = dfs(initial, goal, set(), parent_map, state_map)
    
    if found:
        path = reconstruct_path(end_hash, parent_map, state_map)
        end_time = time.perf_counter()
        print_metrics("DFS", len(path) - 1, metrics["nodes_expanded"], (end_time - metrics["start_time"]) * 1000)
        return path
    return None

def dfs(state, goal, visited, parent_map, state_map):
    state_hash = hash_state(state)
    if state_hash in visited: 
        return False, None
    if check_goal(state, goal): 
        return True, state_hash

    visited.add(state_hash)
    metrics["nodes_expanded"] += 1

    for new_state in generate_states(state):
        new_hash = hash_state(new_state)
        if new_hash not in visited:
            parent_map[new_hash] = state_hash
            state_map[new_hash] = new_state
            found, final_hash = dfs(new_state, goal, visited, parent_map, state_map)
            if found:
                return True, final_hash

    return False, None

def check_goal(state, goal):
    return state == goal

def hash_state(state):
    return "".join(map(str, state))

def generate_states(state: list):
    states=[]
    zero_index=state.index(0)

    if zero_index - 1 >=0 and (zero_index-1) % 3 < 2:
        index=zero_index-1
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    if zero_index + 1 < len(state) and (zero_index+1) % 3 >= 1:
        index=zero_index+1
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    if zero_index + 3 < 9:
        index=zero_index+3  
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    if zero_index -3 >= 0:
        index=zero_index-3
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)

    return states

def reconstruct_path(end_hash, parent_map, state_map):
    path = []
    curr = end_hash
    while curr is not None:
        path.append(state_map[curr])
        curr = parent_map[curr]
    return list(reversed(path))

def print_metrics(algo_name, path_cost, nodes_expanded, running_time):
    print(f"--- {algo_name} Metrics ---")
    print(f"  Path Cost / Depth: {path_cost}")
    print(f"  Nodes Expanded:    {nodes_expanded}")
    print(f"  Running Time:      {running_time:.4f} ms\n")

if __name__=='__main__':
    search([3, 4, 2, 1, 5, 0, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8])