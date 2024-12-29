from board import Board
from bfs import BFSAlgorithm
from ucs import UCSAlgorithm
from HillClimbing import HillClimbingAlgorithm
from dfs import DFSAlgorithm
from a_star import AStarAlgorithm  


class Game:
    def __init__(self, levels_data):
        self.levels = [Level(level_data) for level_data in levels_data]

    def choose_level(self):
        print("Choose a level to play:")
        for i, level in enumerate(self.levels):
            print(f"Level {i + 1}: Board Size {level.board_size}")

        choice = int(input("Enter the level number you want to play: ")) - 1
        if 0 <= choice < len(self.levels):
            self.levels[choice].start()
        else:
            print("Invalid level choice. Please try again.")


class Level:
    def __init__(self, level_data):
        """Initialize a level using provided level data."""
        self.board_size = level_data['board_size']
        self.target_cells = level_data['target_cells']
        self.block_cells = level_data['block_cells']
        self.pieces = level_data['pieces']
        self.board = Board(self.board_size, self.target_cells, self.block_cells, self.pieces)

    def start(self):
        """Start the level."""
        print(f"Starting Level with board size {self.board_size}")
        solve_method = input("Do you want to (M)anually solve the game, use (B)FS, (U)CS, (H)ill Climbing, (D)FS, or (A)* to solve? (M/B/U/H/D/A): ").strip().upper()

        if solve_method in ["B", "BFS"]:
            self.solve_with_bfs()
        elif solve_method in ["U", "UCS"]:
            self.solve_with_ucs()
        elif solve_method in ["H", "HILL"]:
            self.solve_with_hill_climbing()
        elif solve_method in ["D", "DFS"]:
            self.solve_with_dfs()
        elif solve_method in ["A", "A*"]:
            self.solve_with_a_star()
        elif solve_method == "M":
            self.play()
        else:
            print("Invalid choice. Defaulting to manual mode.")
            self.play()

    def solve_with_dfs(self):
        """Solve the level using DFS."""
        print("Solving level using DFS...")
        dfs_solver = DFSAlgorithm(self.board)
        moves = dfs_solver.solve()
        self.display_solution(moves)

    def solve_with_hill_climbing(self):
        """Solve the level using Hill Climbing."""
        print("Solving level using Hill Climbing...")
        hill_solver = HillClimbingAlgorithm(self.board)
        moves = hill_solver.solve()
        self.display_solution(moves)

    def solve_with_ucs(self):
        """Solve the level using UCS."""
        print("Solving level using UCS...")
        ucs_solver = UCSAlgorithm(self.board)
        moves = ucs_solver.solve()
        self.display_solution(moves)

    def solve_with_bfs(self):
        """Solve the level using BFS."""
        print("Solving level using BFS...")
        bfs_solver = BFSAlgorithm(self.board)
        moves = bfs_solver.solve()
        self.display_solution(moves)

    def solve_with_a_star(self):
        """Solve the level using A*."""
        print("Solving level using A*...")
        a_star_solver = AStarAlgorithm(self.board)
        moves = a_star_solver.solve()
        self.display_solution(moves)

    def display_solution(self, moves):
        """Display the solution moves."""
        if moves:
            print("Solution found!")
            for i, (piece, move) in enumerate(moves):
                print(f"Step {i + 1}: Move {piece} to {move}")
                self.board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                self.board.display_board()  # Show the board state after each move
        else:
            print("No solution found.")

    def play(self):
        """Manual game loop for the player."""
        while True:
            self.board.display_board()

            if self.board.check_win_condition():
                print("Congratulations! You've completed the level!")
                break

            try:
                x, y = map(int, input("Enter the coordinates of the piece you want to move (x y): ").strip().split())
                if not self.board.is_within_bounds(x, y) or self.board.grid[x][y] is None:
                    print("Invalid selection. Please select a valid piece.")
                    continue

                new_x, new_y = map(int, input("Enter the new coordinates for the piece (new_x new_y): ").strip().split())
            except ValueError:
                print("Invalid input. Please enter valid integer coordinates, separated by spaces.")
                continue

            if self.board.move_piece(x, y, new_x, new_y):
                print("Piece moved.")
            else:
                print("Invalid move, please try again.")
