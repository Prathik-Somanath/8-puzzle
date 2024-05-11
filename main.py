from node import Node
import numpy as np
import heapq
import time
from copy import deepcopy

class Puzzle:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def movements(self, state):
        movement_arr = []
        blank = np.where(np.array(state) == 0)

        if blank[1] > 0:  # If left movement is possible
            movement_arr.append("left")
        if blank[1] < 2:  # If right movement is possible
            movement_arr.append("right")
        if blank[0] > 0:  # If up movement is possible
            movement_arr.append("up")
        if blank[0] < 2:  # If down movement is possible
            movement_arr.append("down")

        return movement_arr

    def result(self, state, movement):
        position = deepcopy(state)
        blank = np.where(np.array(state) == 0)

        if movement == "up" and blank[0] > 0:  # If UP movement is valid
            position[blank[0], blank[1]] = position[blank[0] - 1, blank[1]]  # Move the blank tile up
            position[blank[0] - 1, blank[1]] = 0  # Set the previous position to 0 (blank)
        elif movement == "down" and blank[0] < 2:  # If DOWN movement is valid
            position[blank[0], blank[1]] = position[blank[0] + 1, blank[1]]  # Move the blank tile down
            position[blank[0] + 1, blank[1]] = 0  # Set the previous position to 0 (blank)
        elif movement == "left" and blank[1] > 0:  # If LEFT movement is valid
            position[blank[0], blank[1]] = position[blank[0], blank[1] - 1]  # Move the blank tile left
            position[blank[0], blank[1] - 1] = 0  # Set the previous position to 0 (blank)
        elif movement == "right" and blank[1] < 2:  # If RIGHT movement is valid
            position[blank[0], blank[1]] = position[blank[0], blank[1] + 1]  # Move the blank tile right
            position[blank[0], blank[1] + 1] = 0  # Set the previous position to 0 (blank)

        return position

    def test_goal(self, state):
        return np.array_equal(state, self.goal_state)

    def cost(self):
    # cost is 1
        return 1

    def child_node(self, parent, movement):
        pos = self.result(parent.state, movement)
        return Node(pos, parent, movement, self.cost())


    def h(self, state, heuristic):
        if heuristic == "misplaced_tiles":
            return np.count_nonzero(state[:-1] != self.goal_state[:-1])  # Count non-matching tiles (excluding the blank tile)
        elif heuristic == "manhattan_distance":
            distance = 0
            for i in range(1, 9):  # Iterate over tiles 1 to 8
                actual_pos = np.where(state == i)  # Get current position of the tile
                goal_pos = np.where(self.goal_state == i)  # Get goal position of the tile
                distance += abs(actual_pos[0] - goal_pos[0]) + abs(actual_pos[1] - goal_pos[1])  # Manhattan distance
            return distance
        else:
            return 0  # Default to 0 if heuristic is not recognized

    def solution(self, node):
        path = []
        while node is not None:
            path.append(node)
            node = node.parent
        return path[::-1]  # reverse
    
def general_search(problem, algo=None):
    node = Node(problem.start_state, None, None, 0)
    if problem.test_goal(node.state):
        return problem.solution(node), 0, 1  # queue size starting from 1
    # Track frontier states
    f_set = set() 
    arr_frontier = []
    priority = node.route_cost + (problem.h(node.state, algo) if algo else 0)
    heapq.heappush(arr_frontier, (priority, node))
    f_set.add(tuple(map(tuple, node.state.tolist())))
    expanded_nodes = 0
    queue_max = 1
    visited = set()
    while arr_frontier:
        _, node = heapq.heappop(arr_frontier)
        f_set.remove(tuple(map(tuple, node.state.tolist())))  # state of node should be removed
        if problem.test_goal(node.state):
            return (problem.solution(node), expanded_nodes, queue_max)
        visited.add(tuple(map(tuple, node.state.tolist())))  # hash
        expanded_nodes += 1
        for movement in problem.movements(node.state):
            child = problem.child_node(node, movement)
            child_tuple = tuple(map(tuple, child.state.tolist()))
            if child_tuple not in visited and child_tuple not in f_set:
                heapq.heappush(arr_frontier, (child.route_cost + (problem.h(child.state, algo) if algo else 0), child))
                f_set.add(child_tuple)  # child state is added
                # If currect length of queue is more than max length of queue then update max queue
                if  queue_max < len(arr_frontier):
                    queue_max = len(arr_frontier)

    return None, expanded_nodes, queue_max
def user_input_puzzle():
    puzzle = []
    for i in range(3):
        row = list(map(int, input(f"Enter the {i+1} row: ").split()))
        puzzle.append(row)
    return np.array(puzzle)

def choose_difficulty():
    print("Select the difficulty level of the puzzle:")
    print("1. Depth 0\n2. Depth 2\n3. Depth 4\n4. Depth 8\n5. Depth 12\n6. Depth 16\n7. Depth 20\n8. Depth 24")
    choice = input()
    if choice == '1':
        return np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    elif choice == '2':
        return np.array([[1, 2, 3], [4, 5, 6], [0, 7, 8]])
    elif choice == '3':
        return np.array([[1, 2, 3], [5, 0, 6], [4, 7, 8]])
    elif choice == '4':
        return np.array([[1, 3, 6], [5, 0, 2], [4, 7, 8]])
    elif choice == '5':
        return np.array([[1, 3, 6], [5, 0, 7], [4, 8, 2]])
    elif choice == '6':
        return np.array([[1, 6, 7], [5, 0, 3], [4, 8, 2]])
    elif choice == '7':
        return np.array([[7, 1, 2], [4, 8, 5], [6, 3, 0]])
    elif choice == '8':
        return np.array([[0, 7, 2], [4, 6, 1], [3, 5, 8]])
    
    else:
        return np.array([[1, 6, 7], [5, 0, 3], [4, 8, 2]])

def main():
    print("Welcome to Prathik's 3x3 8-Puzzle. Type '1' to select default puzzles with difficulty levels, or '2' to create your own puzzle.")
    choice = input()
    if choice == '1':
        default_puzzle = choose_difficulty()
        start_state = default_puzzle
        goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    elif choice == '2':
        print("Enter your puzzle, and blank is denoted by 0. Please enter one row at a time with space to represent columns.")
        start_state = user_input_puzzle()
        goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    else:
        print("Choice is invalid.")
        return

    problem = Puzzle(start_state, goal_state)

    print("Select algorithm.\n(1) Uniform Cost Search\n(2) Misplaced Tile algo\n(3) the Manhattan Distance algo")
    method = input()
    
    if method == '1':
        print("Uniform Cost Search Solution:")
        start_time = time.time()
        solution, expanded_nodes, queue_max = general_search(problem)
    elif method == '2':
        print("A* with Misplaced Tile algo Solution:")
        start_time = time.time()
        solution, expanded_nodes, queue_max = general_search(problem, "misplaced_tiles")
    elif method == '3':
        print("A* with Manhattan Distance algo Solution:")
        start_time = time.time()
        solution, expanded_nodes, queue_max = general_search(problem, "manhattan_distance")
    else:
        print("Invalid choice.")
        return

    end_time = time.time()

    if solution is not None:
        for i, node in enumerate(solution):
            print(f"Puzzle Step {i}:\n", node.state)
        print(f"The Depth of solution: {solution[-1].depth}")
        print(f"Number of nodes expanded: {expanded_nodes}")
        print(f"Max queue size: {queue_max}")
    else:
        print("No solution found.")
    
    print(f"Time taken: {(end_time - start_time) * 1000} ms")

if __name__ == "__main__":
    main()