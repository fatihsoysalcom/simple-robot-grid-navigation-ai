import random

def create_grid(rows, cols, obstacles_count, start, target):
    """Creates a grid with obstacles, a start point, and a target."""
    grid = [['.' for _ in range(cols)] for _ in range(rows)]

    # Place obstacles
    for _ in range(obstacles_count):
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (r, c) != start and (r, c) != target:
            grid[r][c] = '#' # Obstacle

    grid[start[0]][start[1]] = 'R' # Robot start
    grid[target[0]][target[1]] = 'T' # Target
    return grid

def print_grid(grid):
    """Prints the current state of the grid."""
    for row in grid:
        print(" ".join(row))
    print("-" * (len(grid[0]) * 2 - 1))

def get_manhattan_distance(pos1, pos2):
    """Calculates Manhattan distance between two points."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_robot_and_target(grid):
    """Finds the current position of the robot and the target."""
    robot_pos = None
    target_pos = None
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == 'R':
                robot_pos = (r_idx, c_idx)
            elif cell == 'T':
                target_pos = (r_idx, c_idx)
    return robot_pos, target_pos

def move_robot(grid, robot_pos, target_pos):
    """
    Simulates the robot's "AI" decision-making to move towards the target.
    The robot perceives its surroundings and makes a decision.
    """
    r, c = robot_pos
    rows, cols = len(grid), len(grid[0])

    # Possible moves: (dr, dc) for (up, down, left, right)
    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(possible_moves) # Add some randomness if multiple paths are equally good

    best_move = None
    min_distance = float('inf')

    # The robot "perceives" its adjacent cells and evaluates potential moves.
    for dr, dc in possible_moves:
        next_r, next_c = r + dr, c + dc

        # Check if the next position is within bounds and not an obstacle
        if 0 <= next_r < rows and 0 <= next_c < cols and grid[next_r][next_c] != '#':
            # This is where the "AI" decision-making happens:
            # The robot evaluates which move gets it closer to the target.
            new_robot_pos = (next_r, next_c)
            distance_to_target = get_manhattan_distance(new_robot_pos, target_pos)

            if distance_to_target < min_distance:
                min_distance = distance_to_target
                best_move = (next_r, next_c)
            # If distances are equal, a random choice is already handled by shuffling possible_moves

    if best_move:
        # Update the grid: clear current robot position, place robot in new position
        grid[r][c] = '.' # Clear old robot position
        grid[best_move[0]][best_move[1]] = 'R' # Place robot in new position
        return True # Robot moved
    return False # Robot is stuck or no valid moves

# --- Main Simulation ---
if __name__ == "__main__":
    GRID_ROWS = 7
    GRID_COLS = 7
    OBSTACLE_COUNT = 10
    START_POS = (0, 0)
    TARGET_POS = (GRID_ROWS - 1, GRID_COLS - 1)
    MAX_STEPS = 50

    # Initialize the grid
    game_grid = create_grid(GRID_ROWS, GRID_COLS, OBSTACLE_COUNT, START_POS, TARGET_POS)

    print("Initial Grid:")
    print_grid(game_grid)

    robot_current_pos, target_current_pos = find_robot_and_target(game_grid)

    if not robot_current_pos or not target_current_pos:
        print("Error: Robot or Target not found!")
    else:
        print(f"Robot starts at {robot_current_pos}, Target at {target_current_pos}")
        for step in range(MAX_STEPS):
            if robot_current_pos == target_current_pos:
                print(f"Robot reached the target in {step} steps!")
                break

            print(f"Step {step + 1}:")
            moved = move_robot(game_grid, robot_current_pos, target_current_pos)
            print_grid(game_grid)

            if not moved:
                print("Robot is stuck or cannot find a path.")
                break

            robot_current_pos, _ = find_robot_and_target(game_grid) # Update robot's position

        else: # This 'else' belongs to the for loop, executes if loop completes without 'break'
            if robot_current_pos == target_current_pos:
                print(f"Robot reached the target in {MAX_STEPS} steps!")
            else:
                print(f"Max steps ({MAX_STEPS}) reached. Robot did not reach the target.")
