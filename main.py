from node import Node
import numpy as np

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
