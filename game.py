class Piece:
    def __init__(self, color, is_magnetic, position):
        """Initialize piece with its color, magnetic status, and position."""
        self.color = color
        self.is_magnetic = is_magnetic
        self.position = position  # [x, y]

    def __str__(self):
        return f"{self.color[0].upper()}"  # Display first letter of color


class Board:
    def __init__(self, size, targets=None, blocks=None, pieces=None):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]  # 2D grid initialization
        self.targets = targets if targets else []  # List of target positions (goal spots)
        self.blocks = blocks if blocks else []  # List of blocked positions
        self.pieces = []
        
        # Initialize pieces on the board
        if pieces:
            for piece_data in pieces:
                piece = Piece(piece_data['color'], piece_data['is_magnetic'], piece_data['position'])
                self.add_piece(piece, piece_data['position'][0], piece_data['position'][1])

    def add_piece(self, piece, x, y):
        """Add a piece to the board at position (x, y)."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = piece
            self.pieces.append(piece)  # Keep track of pieces on the board
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
                    # Display 'T' for target locations if they are empty
                    row_display += " T " if (i, j) in self.targets else " . "
                else:
                    # Display the piece type
                    row_display += f" {cell} "  
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
        self.grid[new_x][new_y] = self.grid[x][y]
        self.grid[x][y] = None  # Clear original position of the piece
        return True

    def check_win_condition(self):
        """Check if all target positions are occupied by pieces."""
        for (x, y) in self.targets:
            if self.grid[x][y] is None:
                return False
        return True


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
        self.board.display_board()
        # Here you can add the logic to play the level


class Game:
    def __init__(self, levels_data):
        """Initialize the game with levels."""
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


# Example levels data
levels_data = [
    {
        "board_size": 5,
        "target_cells": [[0, 2], [1, 3], [4, 4]],
        "block_cells": [[2, 2], [3, 3],[3, 0]],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [0, 0]},
            {"color": "red", "is_magnetic": true, "position": [0, 4]},
            {"color": "purple", "is_magnetic": true, "position": [1, 1]},
            {"color": "purple", "is_magnetic": true, "position": [1, 2]},
            {"color": "grey", "is_magnetic": false, "position": [2, 1]}
        ]
    },
    {
        "board_size": 4,
        "target_cells": [[1, 1], [1, 3]],
        "block_cells": [],
        "pieces": [
           
            {"color": "purple", "is_magnetic": true, "position": [3, 0]},
            {"color": "grey", "is_magnetic": false, "position": [1, 2]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 2], [2, 0], [2, 2],[2,4],[4,2]],
        "block_cells": [],
        "pieces": [
            {"color": "purple", "is_magnetic": true, "position": [4, 0]},
            {"color": "grey", "is_magnetic": false, "position": [1, 2]},
            {"color": "grey", "is_magnetic": false, "position": [2, 1]},
            {"color": "grey", "is_magnetic": false, "position": [2, 3]},
            {"color": "grey", "is_magnetic": false, "position": [3, 2]}
        ]
    }, 
    {
        "board_size": 4,
        "target_cells": [[0, 3],[2, 3]],
        "block_cells": [[0, 0], [0, 1],[0, 2],[3,0],[3,1],[3,2],[3,3]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [2, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 2]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 0],[0, 2],[4,1]],
        "block_cells": [[0, 3], [0, 4],[1, 3],[1,4],[2,3],[2,4],[3,3],[3,4],[4,3],[4,4],[1,0],[3,0]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [2, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 1]},
            {"color": "grey", "is_magnetic": false, "position": [3, 1]}
        ]
    },
    {
        "board_size": 4,
        "target_cells": [[0, 0],[0, 2]],
        "block_cells": [[0, 3],[1, 3],[2,3],[3,3],[0,1],[1,1],[2,1]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [3, 1]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 0]},
            {"color": "grey", "is_magnetic": false, "position": [2, 0]},
            {"color": "grey", "is_magnetic": false, "position": [1, 2]},
            {"color": "grey", "is_magnetic": false, "position": [2, 2]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 3],[1, 2],[2,3]],
        "block_cells": [[3, 0],[3, 1],[3,2],[3,3],[3,4],[4,0],[4,1],[4,2],[4,3],[4,4]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [2, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 1]},
            {"color": "grey", "is_magnetic": false, "position": [1, 3]}
        ]  
    },
    {
        "board_size": 5,
        "target_cells": [[0, 0],[2, 3],[4,4]],
        "block_cells": [[0, 4],[1, 4],[2,4],[3,4],[4,4],[4,0],[4,1],[4,2]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [2, 1]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 0]},
            {"color": "grey", "is_magnetic": false, "position": [2, 0]},
            {"color": "grey", "is_magnetic": false, "position": [3, 1]},
            {"color": "grey", "is_magnetic": false, "position": [3, 2]}
        ]  
    },
    {
        "board_size": 4,
        "target_cells": [[0, 0],[0, 2],[2,2]],
        "block_cells": [[0, 3],[1, 3],[2,3],[3,3]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [2, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [1, 1]},
            {"color": "grey", "is_magnetic": false, "position": [1, 2]}
        ]  
    }, 
    {
        "board_size": 7,
        "target_cells": [[0, 1],[0, 6]],
        "block_cells": [[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6]],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [0, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [0, 3]},
            {"color": "grey", "is_magnetic": false, "position": [0, 5]}
        ]  
    },
    {
        "board_size": 4,
        "target_cells": [[1, 1],[1, 3],[3,0],[3,3]],
        "block_cells": [],
        "pieces": [
          
            {"color": "purple", "is_magnetic": true, "position": [0, 0]},
          
            {"color": "grey", "is_magnetic": false, "position": [2, 2]},
            {"color": "grey", "is_magnetic": false, "position": [2, 3]},
             {"color": "grey", "is_magnetic": false, "position": [3, 1]}
        ]  
    },
    {
        "board_size": 5,
        "target_cells": [[0, 1],[0, 3],[0,2]],
        "block_cells": [[1,0],[1,1],[1,3],[1,4],[2,2]],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [1, 2]},
            
            {"color": "grey", "is_magnetic": false, "position": [0, 0]},
            {"color": "grey", "is_magnetic": false, "position": [0, 4]}
        ]  
    },
    {
        "board_size": 5,
        "target_cells": [[2, 0],[1, 0],[4,0],[4,2]],
        "block_cells": [[0,4],[1,4],[2,4],[3,4],[4,4],[0,2],[0,3],[1,2],[1,3]],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [3, 1]},
            
            {"color": "grey", "is_magnetic": false, "position": [0, 0]},
            {"color": "grey", "is_magnetic": false, "position": [1, 0]},
             {"color": "grey", "is_magnetic": false, "position": [4, 3]}
        ]  
    },
    {
        "board_size": 6,
        "target_cells": [[0, 3],[1, 1],[2,1]],
        "block_cells": [[1,0],[2,0],[1,4],[1,5],[2,4],[2,5], [3,0],[3,1],[3,2],[3,3],[3,4],[3,5]],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [2, 3]},
            
            {"color": "grey", "is_magnetic": false, "position": [0, 0]},
            {"color": "grey", "is_magnetic": false, "position": [0, 4]},
             {"color": "grey", "is_magnetic": false, "position": [0, 5]}
        ]  
    },
    {
        "board_size": 4,
        "target_cells": [[1, 0],[1, 2],[2,1],[2,2]],
        "block_cells": [],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [3, 3]},
            
            {"color": "grey", "is_magnetic": false, "position": [0, 3]},
            {"color": "grey", "is_magnetic": false, "position": [2, 0]},
             {"color": "grey", "is_magnetic": false, "position": [3, 0]}
        ]  
    },
    {
        "board_size": 5,
        "target_cells": [[0, 0],[0, 2],[1,4],[2,4]],
        "block_cells": [[3,0],[3,1],[3,2],[3,3],[3,4]],
        "pieces": [
            {"color": "red", "is_magnetic": true, "position": [2, 2]},
            
            {"color": "grey", "is_magnetic": false, "position": [0, 1]},
            {"color": "grey", "is_magnetic": false, "position": [0, 3]},
             {"color": "purple", "is_magnetic": true, "position": [1, 2]}
        ]  
    }
]


# Start the game
if __name__ == "__main__":
    game = Game(levels_data)
    game.choose_level()
