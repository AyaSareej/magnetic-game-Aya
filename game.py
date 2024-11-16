<<<<<<< HEAD
class Piece:
    def __init__(self, piece_type, position):
        """Initialize piece with its type and position."""
        self.piece_type = piece_type  # 'repulsive', 'iron', etc.
        self.position = position  # [x, y]

    def __str__(self):
        """Display 'R' for repulsive, 'I' for iron, etc."""
        if self.piece_type == "repulsive":
            return "R"
        elif self.piece_type == "iron":
            return "I"
        elif self.piece_type == "attractive":
            return "A"
        return "?"


class Board:
    def __init__(self, size, targets=None, pieces=None):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]  # 2D grid initialization
        self.targets = targets if targets else []  # List of target positions (goal spots)
        self.pieces = []  # Track all pieces for easy access

        # Initialize pieces on the board
        if pieces:
            for piece_data in pieces:
                piece = Piece(piece_data['piece_type'], piece_data['position'])
                self.add_piece(piece, piece_data['position'][0], piece_data['position'][1])

    def add_piece(self, piece, x, y):
        """Add a piece to the board at position (x, y)."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = piece
            self.pieces.append(piece)
        else:
            print("Position is out of the game boundaries")

    def display_board(self):
        """Display the grid state for the user, marking targets with 'T' if empty."""
        print("Grid game state:")
        print("    " + "  ".join([str(i) for i in range(self.size)]))
        print(" +" + "---" * self.size + "+")
        
        for i, row in enumerate(self.grid):
            row_display = f"{i}| "
            for j, cell in enumerate(row):
                if cell is None:
                    # Display 'T' if it is a target cell and currently empty
                    row_display += " T " if (i, j) in self.targets else " . "
                else:
                    row_display += f" {cell} "  # Display piece type
            row_display += "|"
            print(row_display)
        
        print(" +" + "---" * self.size + "+")

    def is_within_bounds(self, x, y):
        """Check if the coordinates are within the board boundaries."""
        return 0 <= x < self.size and 0 <= y < self.size

    def can_move_piece(self, x, y, new_x, new_y):
        """Check if a piece at (x, y) can move to (new_x, new_y)."""
        if not self.is_within_bounds(x, y) or not self.is_within_bounds(new_x, new_y):
            print("Move out of bounds.")
            return False

        piece = self.grid[x][y]
        if piece is None:
            print("No piece at starting position.")
            return False

        if piece.piece_type == "iron":
            print("Iron pieces cannot be moved manually.")
            return False

        if self.grid[new_x][new_y] is not None:
            print("Target cell is occupied.")
            return False
        
        return True

    def move_piece(self, x, y, new_x, new_y):
        """Move the piece from (x, y) to (new_x, new_y) if valid."""
        if not self.can_move_piece(x, y, new_x, new_y):
            print("Move is not allowed.")
            return False

        # Move the piece to the new location and clear the old spot
        piece = self.grid[x][y]
        self.grid[new_x][new_y] = piece
        self.grid[x][y] = None  # Clear original position of the piece
        piece.position = [new_x, new_y]  # Update piece's internal position
        self.apply_magnetic_effects(new_x, new_y)  # Apply magnetic effects after moving
        return True

    def apply_magnetic_effects(self, x, y):
        """Apply attraction and repulsion effects around the moved piece."""
        piece = self.grid[x][y]
        if piece is None:
            return

        # Define directional offsets
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny):
                target_piece = self.grid[nx][ny]
                if target_piece and target_piece.piece_type == "iron":
                    if piece.piece_type == "attractive":
                        # Move iron piece toward the attractive piece
                        target_x, target_y = x - dx, y - dy
                        if self.is_within_bounds(target_x, target_y) and self.grid[target_x][target_y] is None:
                            self.grid[target_x][target_y] = target_piece
                            self.grid[nx][ny] = None
                            target_piece.position = [target_x, target_y]
                    elif piece.piece_type == "repulsive":
                        # Move iron piece away from the repulsive piece
                        target_x, target_y = nx + dx, ny + dy
                        if self.is_within_bounds(target_x, target_y) and self.grid[target_x][target_y] is None:
                            self.grid[target_x][target_y] = target_piece
                            self.grid[nx][ny] = None
                            target_piece.position = [target_x, target_y]

    def check_win_condition(self):
        """Check if all target positions are occupied by pieces."""
        for (x, y) in self.targets:
            if self.grid[x][y] is None:
                return False
        return True 

=======
from board import Board, Piece 
>>>>>>> main

class Level:
    def __init__(self, level_data):
        """Initialize a level using provided level data."""
        self.board_size = level_data['board_size']
        self.target_cells = [(x[0], x[1]) for x in level_data['target_cells']]
<<<<<<< HEAD
        self.pieces = level_data['pieces']
        self.board = Board(self.board_size, self.target_cells, pieces=self.pieces)
=======
        self.block_cells = [(x[0], x[1]) for x in level_data['block_cells']]
        self.pieces = level_data['pieces']
        self.board = Board(self.board_size, self.target_cells, blocks=self.block_cells, pieces=self.pieces)
>>>>>>> main

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
<<<<<<< HEAD


# Sample levels data
levels_data = [
    {
        "board_size": 4,
        "target_cells": [[1, 1], [1, 3]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 0]},
            {"piece_type": "iron", "position": [1, 2]}
        ]
    },
       {
        "board_size": 5,
        "target_cells": [[0, 2], [2, 0], [2, 2], [4, 2], [2, 4]],
        "pieces": [
            {"piece_type": "repulsive", "position": [4, 0]},
            {"piece_type": "iron", "position": [2, 1],},
            {"piece_type": "iron", "position": [3, 2],},
            {"piece_type": "iron", "position": [1, 2],},
            {"piece_type": "iron", "position": [2, 3],}

        ]
    },
]

# Start the game
if __name__ == "__main__":
    game = Game(levels_data)
    game.choose_level()
=======
>>>>>>> main
