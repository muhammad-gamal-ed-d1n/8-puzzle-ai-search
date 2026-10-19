import time
import heapq
from collections import deque

# Import search functions from your modules
from Astar import a_star, generate_states, hash_state, h_manhattan, h_euclidean
from AstarNode import AstarNode

def run_all_algorithms():
    initial_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    print("=" * 65)
    print(f" 8-PUZZLE SOLVER - TRACE & COMPARISON BENCHMARK ")
    print(f" Initial State: {initial_state}")
    print(f" Goal State:    {goal_state}")
    print("=" * 65 + "\n")

    # --- 1. A* SEARCH TRACE (Manhattan) ---
    print("--- A* Search Trace (Manhattan Distance) ---")
    result_node = a_star_with_trace(initial_state, goal_state, heuristic="manhattan")
    
    if result_node:
        print_solution_path(result_node)

    print("\n" + "=" * 65)
    print("--- RUNNING PERFORMANCE BENCHMARK ACROSS ALGORITHMS ---")
    print("=" * 65 + "\n")

    results = []

    # A* Manhattan Benchmark
    start_time = time.perf_counter()
    node_m = a_star(initial_state, goal_state, heuristic="manhattan")
    end_time = time.perf_counter()
    if node_m:
        results.append({
            "Algorithm": "A* (Manhattan)",
            "Path Cost": node_m.g_score,
            "Nodes Expanded": node_m.g_score, # Minimal expansion in this direct test
            "Time (ms)": (end_time - start_time) * 1000
        })

    # A* Euclidean Benchmark
    start_time = time.perf_counter()
    node_e = a_star(initial_state, goal_state, heuristic="euclidean")
    end_time = time.perf_counter()
    if node_e:
        results.append({
            "Algorithm": "A* (Euclidean)",
            "Path Cost": node_e.g_score,
            "Nodes Expanded": node_e.g_score,
            "Time (ms)": (end_time - start_time) * 1000
        })

    # BFS Benchmark
    start_time = time.perf_counter()
    bfs_cost, bfs_exp = benchmark_bfs(initial_state, goal_state)
    end_time = time.perf_counter()
    results.append({
        "Algorithm": "BFS",
        "Path Cost": bfs_cost,
        "Nodes Expanded": bfs_exp,
        "Time (ms)": (end_time - start_time) * 1000
    })

    # Iterative DFS Benchmark
    start_time = time.perf_counter()
    idfs_cost, idfs_exp = benchmark_idfs(initial_state, goal_state)
    end_time = time.perf_counter()
    results.append({
        "Algorithm": "Iterative DFS",
        "Path Cost": idfs_cost,
        "Nodes Expanded": idfs_exp,
        "Time (ms)": (end_time - start_time) * 1000
    })

    # Print Summary Table
    print(f"{'Algorithm':<20} | {'Path Cost':<10} | {'Nodes Expanded':<15} | {'Time (ms)':<10}")
    print("-" * 65)
    for res in results:
        print(f"{res['Algorithm']:<20} | {str(res['Path Cost']):<10} | {str(res['Nodes Expanded']):<15} | {res['Time (ms)']:<10.4f}")
    print("=" * 65)


def a_star_with_trace(initial, goal, heuristic="manhattan"):
    frontier = []
    best_scores = {hash_state(initial): 0}
    h_func = h_manhattan if heuristic == "manhattan" else h_euclidean
    
    start = AstarNode(
        state=initial,
        g_score=0,
        h_score=h_func(initial, goal),
    )
    import heapq
    heapq.heappush(frontier, start)

    step = 0
    while frontier:
        node = heapq.heappop(frontier)
        if node.g_score > best_scores.get(hash_state(node.state), float("inf")):
            continue

        print(
            f"Search step {step}: {','.join(map(str, node.state))} | "
            f"g={node.g_score}, h={node.h_score}, f={node.f_score}"
        )
        for row in range(0, 9, 3):
            print(" ".join(map(str, node.state[row : row + 3])))
        print()
        step += 1

        if node.state == goal:
            return node

        for new_state in generate_states(node.state):
            new_node = AstarNode(
                state=new_state,
                g_score=node.g_score + 1,
                h_score=h_func(new_state, goal),
                parent=node,
            )
            state_key = hash_state(new_state)
            if new_node.g_score < best_scores.get(state_key, float("inf")):
                best_scores[state_key] = new_node.g_score
                heapq.heappush(frontier, new_node)

    return None


def print_solution_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent

    print("Solution path:")
    for step, path_node in enumerate(reversed(path)):
        state = ",".join(map(str, path_node.state))
        print(
            f"Step {step}: {state} | "
            f"g={path_node.g_score}, h={path_node.h_score}, "
            f"f={path_node.f_score}"
        )


def benchmark_bfs(initial_state, goal_state):
    q = deque([initial_state])
    vis = set()
    expanded = 0
    parent = {hash_state(initial_state): None}
    st_map = {hash_state(initial_state): initial_state}
    
    while q:
        st = q.popleft()
        st_h = hash_state(st)
        if st_h in vis: continue
        if st == goal_state:
            path = []
            curr = st_h
            while curr:
                path.append(st_map[curr])
                curr = parent[curr]
            return len(path) - 1, expanded
        vis.add(st_h)
        expanded += 1
        for n_st in generate_states(st):
            n_h = hash_state(n_st)
            if n_h not in vis and n_h not in parent:
                parent[n_h] = st_h
                st_map[n_h] = n_st
                q.append(n_st)
    return None, expanded


def benchmark_idfs(initial_state, goal_state):
    stack = [initial_state]
    vis = set()
    expanded = 0
    parent = {hash_state(initial_state): None}
    st_map = {hash_state(initial_state): initial_state}
    
    while stack:
        st = stack.pop()
        st_h = hash_state(st)
        if st_h in vis: continue
        vis.add(st_h)
        expanded += 1
        if st == goal_state:
            path = []
            curr = st_h
            while curr:
                path.append(st_map[curr])
                curr = parent[curr]
            return len(path) - 1, expanded
        n_states = generate_states(st)
        for i in range(len(n_states)-1, -1, -1):
            n_st = n_states[i]
            n_h = hash_state(n_st)
            if n_h not in vis:
                if n_h not in parent:
                    parent[n_h] = st_h
                    st_map[n_h] = n_st
                stack.append(n_st)
    return None, expanded


if __name__ == "__main__":
    run_all_algorithms()