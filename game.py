
from board import Board, Piece 

class Level:
    def __init__(self, level_data):
        """Initialize a level using provided level data."""
        self.board_size = level_data['board_size']
        self.target_cells = [(x[0], x[1]) for x in level_data['target_cells']]
        self.pieces = level_data['pieces']
        self.board = Board(self.board_size, self.target_cells, pieces=self.pieces)
        self.block_cells = [(x[0], x[1]) for x in level_data['block_cells']]
        self.pieces = level_data['pieces']
        self.board = Board(self.board_size, self.target_cells, blocks=self.block_cells, pieces=self.pieces)

    def solve_with_bfs(self):
        """Solve the level using BFS."""
        print("Solving level using BFS...")
        moves = self.board.bfs_solve()
        if moves:
            print("Solution found!")
            for i, (piece, move) in enumerate(moves):
                print(f"Step {i + 1}: Move {piece} to {move}")
        else:
            print("No solution found.")

    def start(self):
        """Start the level."""
        print(f"Starting Level with board size {self.board_size}")
        self.play()

    def play(self):
        """Main game loop to allow player to move pieces."""
        while True:
            self.board.display_board()
            
            if self.board.check_win_condition():
                print("Congratulations! You've completed the level!")
                if not self.ask_for_next_action():
                    return  # Exit to level selection

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

    def ask_for_next_action(self):
        """Ask the player whether to restart the level or choose another level."""
        while True:
            action = input("Do you want to (R)estart this level or (C)hoose another level? (R/C): ").strip().upper()
            if action == 'R':
                self.start()  # Restart the current level
                return True
            elif action == 'C':
                return False  # Go back to level selection
            else:
                print("Invalid input. Please enter 'R' or 'C'.")


class Game:
    def __init__(self, levels_data):
        """Initialize the game with levels."""
        self.levels = [Level(level_data) for level_data in levels_data]

    def choose_level(self):
        """Allow the player to choose a level."""
        while True:
            print("Choose a level to play:")
            for i, level in enumerate(self.levels):
                print(f"Level {i + 1}: Board Size {level.board_size}")

            choice = int(input("Enter the level number you want to play: ")) - 1
            if 0 <= choice < len(self.levels):
                self.levels[choice].start()
            else:
                print("Invalid level choice. Please try again.")



