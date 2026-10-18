import heapq
from AstarNode import AstarNode

def a_star(initial, goal):

    frontier = []

    # keep track of best g_scores
    best_scores = {}
    best_scores[hash_state(initial)] = 0

    # choosing heuristic 
    h = h_manhattan
    start = AstarNode(state=initial, 
                      g_score=0,
                      h_score=h(initial))

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
            new_state_node = AstarNode(state=new_state, g_score=node.g_score+1, h_score=h(new_state), parent=node)

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

def h_manhattan(state):
    h = 0
    # sum of absolute distance between current state and goal
    for i in range(0, 9):
        h += abs(i - state[i])
    return h


if __name__=='__main__':
    result = a_star([1,2,5,3,4,0,6,7,8], [0,1,2,3,4,5,6,7,8])
    print(result.state)
    print(result.g_score)
    print(result.h_score)
    print(result.f_score)