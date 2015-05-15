from p6_game import Simulator

ANALYSIS = {}

def graph(sim, state, moves):
    edges = []

    for move in moves:
        nextState = sim.get_next_state(state, move)

        if nextState:
            edges.append(nextState)

    return edges

def analyze(design):
    ANALYSIS.clear()
    sim = Simulator(design)
    init = sim.get_initial_state()
    moves = sim.get_moves()
    queue = [init]
    ANALYSIS[init] = None

    while queue:
        node = queue.pop(0)

        for nextNode in graph(sim, node, moves):
            if nextNode not in ANALYSIS:
                queue.append(nextNode)
                ANALYSIS[nextNode] = node

def inspect((i, j), draw_line):
    for state in ANALYSIS:
        if (i, j) == state[0]:
            node = state
            offset = state[1]

            while node:
                prevNode = None

                if ANALYSIS.get(node):
                    prevNode = ANALYSIS[node]
                    draw_line(node[0], prevNode[0], offset_obj=offset, color_obj=prevNode[1])

                node = ANALYSIS[node]
            print(state[1])

    print("")
