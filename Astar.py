import heapq
import math
from AstarNode import AstarNode

def a_star(initial, goal, heuristic="manhattan"):

    frontier = []

    # keep track of best g_scores
    best_scores = {}
    best_scores[hash_state(initial)] = 0

    h_func = h_manhattan if heuristic == "manhattan" else h_euclidean

    start = AstarNode(state=initial, 
                      g_score=0,
                      h_score=h_func(initial, goal))

    # push node to heap
    heapq.heappush(frontier, start)

    while frontier:
        node = heapq.heappop(frontier)

        if check_goal(node.state, goal):
            return node

        # if node's score is worse than best then no need to expand it
        # this prevents redundant check and infinite loops
        if node.g_score > best_scores.get(hash_state(node.state), float('inf')):
            continue

        new_states = generate_states(node.state)
        for new_state in new_states:
            new_state_node = AstarNode(
                state=new_state,
                g_score=node.g_score + 1,
                h_score=h_func(new_state, goal),
                parent=node,
            )

            # if score is better than that of old node (or if entry is not present) update it
            # else let node go
            if new_state_node.g_score < best_scores.get(hash_state(new_state), float('inf')):
                best_scores[hash_state(new_state)] = new_state_node.g_score
                heapq.heappush(frontier, new_state_node)

    return None


def check_goal(state, goal):
    return state == goal

def hash_state(state):
    hashed=""
    for num in state:
        hashed+=str(num)
    return hashed

def generate_states(state: list):
    states=[]
    
    zero_index=state.index(0)

    # swap with left if it doesn't lead to % 3 == 2 
    if zero_index - 1 >=0 and (zero_index-1) % 3 < 2:
        index=zero_index-1
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    
    # swap with right if it doesn't lead to % 3 == 0
    if zero_index + 1 < len(state) and (zero_index+1) % 3 >= 1:
        index=zero_index+1
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    
    # swap upwards if array limit not exceeded
    if zero_index + 3 < 9:
        index=zero_index+3  
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)
    
    
    # swap with below if array limit not exceeded
    if zero_index -3 >= 0:
        index=zero_index-3
        new_state=state.copy()
        new_state[zero_index], new_state[index] = new_state[index], new_state[zero_index]
        states.append(new_state)

    return states

def h_manhattan(state, goal):
    h = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = goal.index(tile)
        h += abs(index // 3 - goal_index // 3)
        h += abs(index % 3 - goal_index % 3)
    return h

def h_euclidean(state, goal):
    h = 0.0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = goal.index(tile)
        x1, y1 = index % 3, index // 3
        x2, y2 = goal_index % 3, goal_index // 3
        h += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return h


if __name__=='__main__':
    result = a_star([1,2,5,3,4,0,6,7,8], [0,1,2,3,4,5,6,7,8], heuristic="manhattan")
    if result is None:
        print("No solution found.")
    else:
        path = []
        while result is not None:
            path.append(result)
            result = result.parent

        for step, node in enumerate(reversed(path)):
            state = ",".join(map(str, node.state))
            print(
                f"Step {step}: {state} | "
                f"g={node.g_score}, h={node.h_score}, f={node.f_score}"
            )