def e1(state):
    if state[0] > 0:
        state[0] = 0
        return True

def e2(state):
    if state[1] > 0:
        state[1] = 0
        return True

def f1(state):
    if state[0] < 4:
        state[0] = capacity[0]
        return True

def f2(state):
    if state[1] < 3:
        state[1] = capacity[1]
        return True

def t12a(state):
    if state[0] + state[1] <= 3 and state[0] > 0:
        state[1] += state[0]
        state[0] = 0
        return True

def t12b(state):
    if state[0] + state[1] > 3 and state[1] < 3:
        state[0] -= (capacity[1] - state[1])
        state[1] = capacity[1]
        return True

def t21a(state):
    if state[0] + state[1] <= 4 and state[1] > 0:
        state[0] += state[1]
        state[1] = 0
        return True

def t21b(state):
    if state[0] + state[1] > 4 and state[0] < 4:
        state[1] -= (capacity[0] - state[0])
        state[0] = capacity[0]
        return True

def equal_state(s1, s2):
    return s1[0] == s2[0] and s1[1] == s2[1]

def copy_state(s):
    return [s[0], s[1]]

def get_state_str(state, op):
    return str(state[0]) + "-" + str(state[1]) + "-" + op.__name__

# info
initial_state = [0, 0]
capacity = [4, 3]
target = [2, 0]

# list of valid operators
operators = [e1, e2, f1, f2, t12a, t12b, t21a, t21b]

# put valid operations from the initial state in the stack
stack = []
seen = set()
for op in operators:
    if op(copy_state(initial_state)):
        stack.append((copy_state(initial_state), op, []))
        seen.add(get_state_str(initial_state, op))


while True:
    # get next operation
    curr_state, op, previous_ops = stack.pop()

    # check if reached target
    if equal_state(curr_state, target):
        print("found solution: ", previous_ops)
        break

    # apply operation and store it
    op(curr_state)
    op_sequence = [op for op in previous_ops]
    op_sequence.append(op.__name__)

    # put valid operations in the stack
    for op in operators:
        # check it is not a repeated state
        state_str = get_state_str(curr_state, op)
        if state_str in seen:
            continue
        seen.add(state_str)

        test = op(copy_state(curr_state))
        if test:
            stack.append((copy_state(curr_state), op, op_sequence))
