def input_puzzle():
    print("Enter the initial state of the 8 puzzle(0 represents blank space):")
    puzzle = []
    for i in range(3):
        row = input(f"Enter values for row {i+1}: ").strip().split()
        if len(row) != 3:
            print("Please enter exactly 3 values for each row.")
            return input_puzzle()
        row = [int(num) for num in row]
        puzzle.append(row)
    return puzzle

initial_state = input_puzzle()
print("Initial State:", initial_state)
