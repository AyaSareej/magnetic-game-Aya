class Piece:
    def __init__(self, magnetic_type):
        """Initialize piece with its magnetic type"""
        self.magnetic_type = magnetic_type  

    def __str__(self):
        return self.magnetic_type[0].upper()  


class Board:
    def __init__(self, size, targets=None):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]  
        self.targets = targets if targets else []  

    def add_piece(self, piece, x, y):
        """Add a piece to the board at position (x, y)"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = piece
        else:
            print("Position is out of the game boundaries")

    def display_board(self):
        """Display the grid state for the user, marking targets with 'T' if empty"""
        print("Grid game state:")
        print("    " + "  ".join([str(i) for i in range(self.size)]))
        print(" +" + "---" * self.size + "+")
        
        for i, row in enumerate(self.grid):
            row_display = f"{i}| "
            for j, cell in enumerate(row):
                if cell is None:
                    
                    row_display += " T " if (i, j) in self.targets else " . "
                else:
                    
                    if cell.magnetic_type == "Attracts":
                        row_display += " . "  
                    else:
                        row_display += f" {cell} "  
            row_display += "|"
            print(row_display)
        
        print(" +" + "---" * self.size + "+")

    def is_within_bounds(self, x, y):
        """Check if the coordinates are within the board boundaries"""
        return 0 <= x < self.size and 0 <= y < self.size

    def can_move_piece(self, x, y, new_x, new_y):
        """Check if a piece at (x, y) can move to (new_x, new_y)"""
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
        """Move the piece from (x, y) to (new_x, new_y) if valid"""
        if not self.can_move_piece(x, y, new_x, new_y):
            print("Move is not allowed.")
            return False

        piece = self.grid[x][y]
        if piece.magnetic_type == "Repels":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
                adjacent_x, adjacent_y = new_x + dx, new_y + dy
                if self.is_within_bounds(adjacent_x, adjacent_y):
                    adjacent_piece = self.grid[adjacent_x][adjacent_y]
                    if adjacent_piece and adjacent_piece.magnetic_type == "Iron piece":
                        self.move_iron_piece(adjacent_x, adjacent_y, dx, dy)

        self.grid[new_x][new_y] = self.grid[x][y]
        self.grid[x][y] = None  
        return True

    def move_iron_piece(self, x, y, dx, dy):
        """Move the Iron piece away from the Repels piece"""
        new_x = x + dx
        new_y = y + dy
        if self.is_within_bounds(new_x, new_y) and self.grid[new_x][new_y] is None:
            self.grid[new_x][new_y] = self.grid[x][y]
            self.grid[x][y] = None  
            print(f"Iron piece moved from ({x}, {y}) to ({new_x}, {new_y}) due to repulsion.")

    def check_win_condition(self):
        """Check if all target positions are occupied by pieces"""
        for (x, y) in self.targets:
            if self.grid[x][y] is None:
                return False
        return True

    def validate_targets(self):
        """Ensure target count matches the total magnetic pieces that should occupy them"""
        magnetic_pieces_count = sum(
            1 for row in self.grid for piece in row if piece and piece.magnetic_type in {"Attracts", "Iron piece"}
        )
        if len(self.targets) != magnetic_pieces_count:
            print(f"Error: Mismatch between targets ({len(self.targets)}) and magnetic pieces ({magnetic_pieces_count})")
            return False
        return True


class Game:
    def __init__(self):
        self.board = self.initialize_board()

    def initialize_board(self):
        """Initialize the board and pieces to the starting state"""
        targets = [(3, 3), (4, 4)]
        board = Board(5, targets)
        board.add_piece(Piece("Repels"), 1, 1)
        board.add_piece(Piece("Iron piece"), 2, 2)
        return board

    def play(self):
        """Main game loop to allow player to move pieces"""
        while not self.board.check_win_condition():
            self.board.display_board()

            try:
                x, y = map(int, input("Enter the coordinates of the piece you want to move (x y): ").strip().split())
                new_x, new_y = map(int, input("Enter the new coordinates for the piece (new_x new_y): ").strip().split())
            except ValueError:
                print("Invalid input. Please enter valid integer coordinates, separated by spaces.")
                continue

            if self.board.move_piece(x, y, new_x, new_y):
                print("Piece moved.")
            else:
                print("Invalid move, please try again.")
            
            if self.board.check_win_condition():
                print("Congratulations! All target positions are filled!")
                self.board.display_board()
                break


if __name__ == "__main__":
    game = Game()
    game.play()
