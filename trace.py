import heapq

from Astar import generate_states, hash_state, h_manhattan
from AstarNode import AstarNode


def a_star_with_trace(initial, goal):
    frontier = []
    best_scores = {hash_state(initial): 0}
    start = AstarNode(
        state=initial,
        g_score=0,
        h_score=h_manhattan(initial, goal),
    )
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
        step += 1

        if node.state == goal:
            return node

        for new_state in generate_states(node.state):
            new_node = AstarNode(
                state=new_state,
                g_score=node.g_score + 1,
                h_score=h_manhattan(new_state, goal),
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

    print("\nSolution path:")
    for step, path_node in enumerate(reversed(path)):
        state = ",".join(map(str, path_node.state))
        print(
            f"Step {step}: {state} | "
            f"g={path_node.g_score}, h={path_node.h_score}, "
            f"f={path_node.f_score}"
        )


if __name__ == "__main__":
    initial_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    print("A* search trace (states removed from the priority queue):")
    result = a_star_with_trace(initial_state, goal_state)
    if result is None:
        print("No solution found.")
    else:
        print_solution_path(result)
