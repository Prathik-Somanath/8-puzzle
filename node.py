import numpy as np

class Node:
    def __init__(self, state, parent, movement, route_cost):
        self.state = state
        self.movement = movement
        self.parent = parent
        # increasing the parent node depth
        self.depth = parent.depth + 1 if parent is not None else 0
        self.route_cost = parent.route_cost + route_cost if parent is not None else 0

    def __eq__(self, other):
        return isinstance(other, Node) and np.array_equal(self.state, other.state)

    def __lt__(self, other):
        return other.route_cost > self.route_cost