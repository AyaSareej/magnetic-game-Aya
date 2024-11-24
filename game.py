from board import Board
from bfs import BFSAlgorithm
from ucs import UCSAlgorithm  # Import UCS Algorithm


class Game:
    def __init__(self, levels_data):
        self.levels = [Level(level_data) for level_data in levels_data]

    def choose_level(self):
        """Allow the player to choose a level."""
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
        solve_method = input("Do you want to (M)anually solve the game, use (B)FS, or (U)CS to solve? (M/B/U): ").strip().upper()

        if solve_method in ["B", "BFS"]:
            self.solve_with_bfs()
        elif solve_method in ["U", "UCS"]:
            self.solve_with_ucs()
        elif solve_method == "M":
            self.play()
        else:
            print("Invalid choice. Defaulting to manual mode.")
            self.play()

    def solve_with_ucs(self):
        """Solve the level using UCS."""
        print("Solving level using UCS...")
        ucs_solver = UCSAlgorithm(self.board)
        moves = ucs_solver.solve()
        if moves:
            print("Solution found!")
            for i, (piece, move) in enumerate(moves):
                print(f"Step {i + 1}: Move {piece} to {move}")
            # Apply moves to visualize solution
            for piece, move in moves:
                self.board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                self.board.display_board()  # Show the board state after each move
 

    def solve_with_bfs(self):
        """Solve the level using BFS."""
        print("Solving level using BFS...")
        bfs_solver = BFSAlgorithm(self.board)
        moves = bfs_solver.solve()
        if moves:
            print("Solution found!")
            for i, (piece, move) in enumerate(moves):
                print(f"Step {i + 1}: Move {piece} to {move}")
            # Apply moves to visualize solution
            for piece, move in moves:
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
