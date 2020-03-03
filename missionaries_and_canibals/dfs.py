def gg_wp(state):
    return (state[0][1] > state[0][0] and state[0][0] != 0) or (state[1][1] > state[1][0] and state[1][0] != 0)

def move_person(state, p, op, margin):
    state[margin][p] += op
    return False if gg_wp(state) else True

def travel(state, p1, p2, next_margin):
    if state[2] == next_margin: return False # check if on correct margin to apply operator
    miss_count = sum([1 if p==0 else 0 for p in [p1,p2]])
    can_count = sum([1 if p==1 else 0 for p in [p1,p2]])

    # check if enough people on the margin
    if miss_count > state[state[2]][0] or can_count > state[state[2]][1]: return False

    new_state = [
        [state[0][0], state[0][1]],
        [state[1][0], state[1][1]],
        state[2]
    ]

    # enter the boat and check missionary-canibal balance. canibal enters first
    if not move_person(new_state, 1, -can_count, state[2]): return False
    if not move_person(new_state, 0, -miss_count, state[2]): return False
    
    # leave the boat. missionary leaves first
    if not move_person(new_state, 0, miss_count, next_margin): return False
    if not move_person(new_state, 1, can_count, next_margin): return False
    
    new_state[2] = next_margin
    return new_state

def copy_state(s):
    return [
        [s[0][0], s[0][1]],
        [s[1][0], s[1][1]],
        s[2]
    ]

def get_state_str(state, config):
    return str(state)+str(config)

def get_state_msg(state):
    msg = "Margin 1: "
    msg += str(state[0][0]) + "," + str(state[0][1]) + "; Margin 2: "
    msg += str(state[1][0]) + "," + str(state[1][1])
    msg += ". " + "Curr margin: " + str(state[2]+1) + "\n"
    return msg

# state = [ [miss1, can1], [miss2, can2], curr_margin]
init_state = [[3,3],[0,0], 0]

# list of valid operations [margin, p1, p2]
travel_options = [
    [0, 0, None],
    [0, 1, None],
    [0, 0, 0],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, None],
    [1, 1, None],
    [1, 0, 0],
    [1, 1, 0],
    [1, 1, 1]
]

seen = set()

# put valid operations from the initial state in the queue
stack = []
for config in travel_options:
    cpy = copy_state(init_state)
    res = travel(cpy, config[1], config[2], config[0])
    if res != False:
        stack.append((cpy, config, get_state_msg(cpy)))
        seen.add(get_state_str(cpy, config))

while True:
    # get next operation
    curr_state, config, previous_ops = stack.pop()

    # check if reached target
    if curr_state[1][0] == 3 and curr_state[1][1] == 3:
        print("found solution\n", previous_ops)
        break

    # apply operation and store it
    new_state = travel(curr_state, config[1], config[2], config[0])
    op_sequence = previous_ops + get_state_msg(new_state)

    # put valid operations in the queue
    for next_config in travel_options:
        cpy = copy_state(new_state)

        state_str = get_state_str(cpy, next_config)
        if state_str in seen:
            continue
        seen.add(state_str)

        res = travel(cpy, next_config[1], next_config[2], next_config[0])
        if res != False:
            stack.append((cpy, next_config, op_sequence))

