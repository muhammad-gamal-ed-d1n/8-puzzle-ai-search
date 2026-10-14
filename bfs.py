from collections import deque

def search(initial, goal):
    queue = deque([initial])

    visited=set()
    while queue:
        state=queue.popleft()
        print(state)

        if (check_goal(state, goal)):
            # print(state) 
            return True

        visited.add(hash_state(state))

        new_states=generate_states(state)
        for new_state in new_states:
            if hash_state(new_state) not in visited:
                queue.append(new_state)

    return False


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


if __name__=='__main__':
    print(search([1,2,5,3,4,0,6,7,8], [0,1,2,3,4,5,6,7,8]))