from collections import deque
from bfs import BFSAlgorithm

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
    def __init__(self, size, targets=None, blocks=None, pieces=None):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]  # 2D grid initialization
        self.targets = targets if targets else []  # List of target positions (goal spots)
        self.blocks = blocks if blocks else []  # List of block positions
        self.pieces = []  # Track all pieces for easy access

        # Initialize pieces on the board
        if pieces:
            for piece_data in pieces:
                piece = Piece(piece_data['piece_type'], piece_data['position'])
                self.add_piece(piece, piece_data['position'][0], piece_data['position'][1])

        # Add blocks to the board
        for block in self.blocks:
            self.add_block(block[0], block[1])

        # for algorithms
        self.states = []
        self.save_state()

        # 
        # in board class
        # 
    def get_grid(self):
            """Returns the current grid state."""
            return self.grid
    
    def all_targets_filled(self):
        """Check if all target positions are occupied by valid pieces."""
        for x, y in self.targets:
            piece = self.grid[x][y]
            if piece is None or not isinstance(piece, Piece):  # Ensure a valid piece is present
                return False
        return True

    def get_state(self):
        """
        Get a hashable representation of the board's current state.
        Includes grid, pieces, blocks, and target positions.
        """
        # Capture grid state
        grid_state = tuple(tuple(cell for cell in row) for row in self.grid)

        # Capture piece states
        pieces_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.pieces))

        # Include block and target positions
        blocks_state = tuple(sorted(self.blocks))
        targets_state = tuple(sorted(self.targets))

        return (grid_state, pieces_state, blocks_state, targets_state)


    def save_state(self):
        grid_copy = [row[:] for row in self.grid]
        self.states.append(grid_copy)

    def has_reached_state(self, grid):
        return any(grid == state for state in self.states)
    
    def set_state(self, state):
        """Restore the board and pieces from a given state."""
        board_state, piece_state = state

        # Reset grid
        self.grid = [list(row) for row in board_state]

        # Reset pieces
        for piece in self.pieces:
            for piece_type, position in piece_state:
                if piece.piece_type == piece_type:
                    piece.position = list(position)
                    x, y = position
                    self.grid[x][y] = piece

    def get_valid_moves_for_piece(self, piece):
        """Get all valid moves for a specific piece."""
        x, y = piece.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        valid_moves = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.can_move_piece(x, y, new_x, new_y):
                valid_moves.append((new_x, new_y))

        return valid_moves


#
#
#
    # def get_state(self):
    #     """
    #     Get the current state of the board and pieces.
    #     This will be a tuple containing:
    #     - A tuple for each piece (type, position).
    #     - A tuple for all blocks (to differentiate states with blocks).
    #     - A tuple for the targets (to differentiate by target setup).
    #     """
    #     pieces_state = tuple((piece.piece_type, tuple(piece.position)) for piece in self.pieces)
    #     blocks_state = tuple(sorted(self.blocks))  # Sort to make it hashable
    #     targets_state = tuple(sorted(self.targets))  # Sort to make it hashable
    #     return (pieces_state, blocks_state, targets_state)

    # def set_state(self, state):
    #     """
    #     Restore the board to a specific state.
    #     Input `state` is a tuple containing:
    #     - A tuple for each piece (type, position).
    #     - A tuple for all blocks.
    #     - A tuple for the targets.
    #     """
    #     pieces_state, blocks_state, targets_state = state

    #     # Reset the grid and pieces
    #     self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
    #     self.pieces = []
    #     self.blocks = list(blocks_state)
    #     self.targets = list(targets_state)

    #     # Add pieces back to the grid
    #     for piece_type, position in pieces_state:
    #         piece = Piece(piece_type, list(position))
    #         self.add_piece(piece, position[0], position[1])

    #     # Add blocks to the grid
    #     for block in self.blocks:
    #         self.add_block(block[0], block[1])

    
    # def is_valid_move(self, piece, new_pos):
    #         x, y = new_pos
    #         return (0 <= x < self.board_size and 
    #                 0 <= y < self.board_size and 
    #                 self.board[x][y] is None)
    
    # def find_piece_by_type(self, piece_type, position):
    #     """Find a piece by its type and position."""
    #     for piece in self.pieces:
    #         if piece.piece_type == piece_type and tuple(piece.position) == position:
    #             return piece
    #     return None



    # def get_all_valid_moves(self):
    #     """Get all valid moves for all pieces."""
    #     valid_moves = {}
    #     for piece in self.pieces:
    #         if piece.piece_type == "iron":  # Iron pieces cannot be moved manually
    #             continue
    #         valid_moves[piece] = self.get_valid_moves_for_piece(piece)
    #     return valid_moves

    # def get_valid_moves_for_piece(self, piece):
    #     """Get all valid moves for a specific piece."""
    #     x, y = piece.position
    #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    #     valid_moves = []

    #     for dx, dy in directions:
    #         new_x, new_y = x + dx, y + dy
    #         if self.can_move_piece(x, y, new_x, new_y):
    #             valid_moves.append((new_x, new_y))

    #     return valid_moves

    # def simulate_move(self, piece, move):
    #     """Simulate a move and return the resulting state."""
    #     x, y = piece.position
    #     new_x, new_y = move

    #     # Temporarily apply the move
    #     original_grid = [row[:] for row in self.grid]  # Copy grid
    #     original_position = piece.position[:]

    #     self.move_piece(x, y, new_x, new_y)
    #     new_state = self.get_state()

    #     # Revert to the original state
    #     self.grid = original_grid
    #     piece.position = original_position

    #     return new_state

    # def check_win_condition(self):
    #     """Check if all target positions are occupied by pieces."""
    #     for (x, y) in self.targets:
    #         piece = self.grid[x][y]
    #         if piece is None or not isinstance(piece, Piece):
    #             return False
    #     return True

    
    # def find_piece_by_type(self, piece_type, position):
    #     """Find a piece by its type and position."""
    #     for piece in self.pieces:
    #         if piece.piece_type == piece_type and tuple(piece.position) == position:
    #             return piece
    #     return None



            # 
            # 
            # 

    def move_adjacent_pieces_towards(self, new_position):
        """Pull adjacent pieces towards the attractive piece."""
        x, y = new_position

        # Check and move pieces from left
        for j in range(y-1, -1, -1):
            piece = self.grid[x][j]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((x,j), (x,j+1))

        # Check and move pieces from right
        for j in range(y + 1, self.size):
            piece = self.grid[x][j]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((x, j), (x, j-1))

        # Check and move pieces from above
        for i in range(x-1, -1, -1):
            piece = self.grid[i][y]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((i,y), (i+1, y))

        # Check and move pieces from below
        for i in range(x+1, self.size):
            piece = self.grid[i][y]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((i, y), (i-1, y))
    
    def move_adjacent_pieces_away(self, new_position):
        """Push adjacent pieces away from the repulsive piece."""
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            x, y = new_position
            while True:
                x1, y1 = x, y

                if direction == "up":
                    x -= 1
                elif direction == "down":
                    x += 1
                elif direction == "left":
                    y -= 1
                elif direction == "right":
                    y += 1

                if not self.is_within_bounds(x, y):
                    break

                if self.grid[x][y] is not None and self.grid[x][y] != 'X':
                    connected_pieces = self.get_connected_pieces((x1, y1), direction)
                    if connected_pieces:
                        self.move_connected_pieces_away((x1, y1), direction)
                    break
    
    def get_connected_pieces(self, start_position, direction):
        """Get list of connected pieces in a direction."""
        connected = []
        x, y = start_position
        
        while True:
            if direction == "up":
                x -= 1
            elif direction == "down":
                x += 1
            elif direction == "left":
                y -= 1
            elif direction == "right":
                y += 1

            if not self.is_within_bounds(x, y) or self.grid[x][y] is None:
                break

            connected.append((x, y))
            
        return connected
    
    def move_connected_pieces_away(self, start_position, direction):
        """Move connected pieces away from the repulsive piece."""
        connected_pieces = self.get_connected_pieces(start_position, direction)
        if not connected_pieces:
            return False

        last_piece_pos = connected_pieces[-1]
        lx, ly = last_piece_pos

        # Calculate the position after the last piece
        if direction == "up":
            after_position = (lx-1, ly)
        elif direction == "down":
            after_position = (lx+1, ly)
        elif direction == "left":
            after_position = (lx, ly-1)
        elif direction == "right":
            after_position = (lx, ly+1)

        # Move pieces if possible
        if self.is_within_bounds(after_position[0], after_position[1]) and self.grid[after_position[0]][after_position[1]] is None:
            for pos in reversed(connected_pieces):
                self.move_piece_away(pos, direction)
            return True
        return False

    def move_piece_away(self, current_position, direction):
        """Move a single piece away in the specified direction."""
        cx, cy = current_position
        
        if direction == "up":
            new_position = (cx-1, cy)
        elif direction == "down":
            new_position = (cx+1, cy)
        elif direction == "left":
            new_position = (cx, cy-1)
        elif direction == "right":
            new_position = (cx, cy+1)

        if self.is_within_bounds(new_position[0], new_position[1]) and self.grid[new_position[0]][new_position[1]] is None:
            piece = self.grid[cx][cy]
            if isinstance(piece, Piece):
                self.grid[cx][cy] = None
                piece.position = [new_position[0], new_position[1]]
                self.grid[new_position[0]][new_position[1]] = piece

    def add_piece(self, piece, x, y):
        """Add a piece to the board at position (x, y)."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = piece
            self.pieces.append(piece)
        else:
            print("Position is out of the game boundaries")

    def add_block(self, x, y):
        """Add a block to the board at position (x, y)."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = 'X'  # Mark the block position
            print(f"Block added at ({x}, {y})")  # Debugging output
        else:
            print("Block position is out of the game boundaries")


    def display_board(self):
        """Display the grid state for the user, marking targets with 'T' if empty and blocks with 'X'."""
        print("Grid game state:")
        print("    " + "  ".join([str(i) for i in range(self.size)]))
        print(" +" + "---" * self.size + "+")

        for i, row in enumerate(self.grid):
            row_display = f"{i}| "
            for j, cell in enumerate(row):
                if (i, j) in self.targets and cell is None:
                    # Show target 'T' if it is empty
                    row_display += " T "
                elif (i, j) in self.blocks:
                    # Show block 'X'
                    row_display += " X "
                elif cell is None:
                    # Show empty cell
                    row_display += " . "
                else:
                    # Show the piece (e.g., 'I', 'R', 'A')
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

        if piece.piece_type == "iron":
            print("Iron pieces cannot be moved manually.")
            return False

        if self.grid[new_x][new_y] is not None:
            print("Target cell is occupied.")
            return False
        
        if self.grid[new_x][new_y] == 'X':
            print("Cannot move to a block cell.")
            return False

        return True

    def can_repel_piece(self, piece, target_x, target_y):
        """Check if a piece can repel another piece considering blocks."""
        if self.grid[target_x][target_y] == 'X':
            print("Cannot repel due to a block cell.")
            return False
        return True
    
    def push_connected_iron_pieces_away(self, x, y):
        """Push connected iron pieces away from the repulsive piece if possible."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Check adjacent cells
            if self.is_within_bounds(nx, ny):
                target_piece = self.grid[nx][ny]
                if isinstance(target_piece, Piece) and target_piece.piece_type == "iron":
                    # Move the iron piece away from the repulsive piece
                    target_new_x, target_new_y = x - dx, y - dy  # Move iron piece away from repulsive piece
                    if self.is_within_bounds(target_new_x, target_new_y) and self.grid[target_new_x][target_new_y] is None:
                        # Move the iron piece
                        self.grid[target_new_x][target_new_y] = target_piece
                        self.grid[nx][ny] = None
                        target_piece.position = [target_new_x, target_new_y]

    def move_piece(self, x, y, new_x, new_y):
        """Move the piece from (x, y) to (new_x, new_y) if valid."""
        if not self.can_move_piece(x, y, new_x, new_y):
            print("Move is not allowed.")
            return False

        piece = self.grid[x][y]
        self.grid[new_x][new_y] = piece
        self.grid[x][y] = None  # Clear original position of the piece
        piece.position = [new_x, new_y]  # Update piece's internal position

        # Apply magnetic effects based on piece type
        if piece.piece_type == "attractive":
            self.move_adjacent_pieces_towards((new_x, new_y))
        elif piece.piece_type == "repulsive":
            self.move_adjacent_pieces_away((new_x, new_y))

        self.save_state()

        return True
        
    def move_piece_to(self, current_position, new_position):
        """Helper method to move a piece to a new position."""
        if self.is_within_bounds(new_position[0], new_position[1]) and self.grid[new_position[0]][new_position[1]] is None:
            piece = self.grid[current_position[0]][current_position[1]]
            if isinstance(piece, Piece):
                self.grid[current_position[0]][current_position[1]] = None
                piece.position = [new_position[0], new_position[1]]
                self.grid[new_position[0]][new_position[1]] = piece

    def pull_adjacent_iron_pieces(self, x, y):
        """Pull adjacent iron pieces towards the attractive piece if possible."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Check adjacent cells
            if self.is_within_bounds(nx, ny):
                target_piece = self.grid[nx][ny]
                if isinstance(target_piece, Piece) and target_piece.piece_type == "iron":
                    # Try to move the iron piece towards the attractive piece
                    target_new_x, target_new_y = x + dx, y + dy  # Move iron piece towards attractive piece
                    if self.is_within_bounds(target_new_x, target_new_y) and self.grid[target_new_x][target_new_y] is None:
                        # Move the iron piece
                        self.grid[target_new_x][target_new_y] = target_piece
                        self.grid[nx][ny] = None
                        target_piece.position = [target_new_x, target_new_y]

    def apply_magnetic_effects(self, x, y):
        """Apply attraction and repulsion effects around the moved piece."""
        piece = self.grid[x][y]
        if piece is None:
            return

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny):
                target_piece = self.grid[nx][ny]
                if isinstance(target_piece, Piece):  # Check if target is a Piece object
                    if target_piece.piece_type == "iron":
                        if piece.piece_type == "attractive":
                            self.pull_adjacent_iron_pieces(x, y)
                        elif piece.piece_type == "repulsive":
                            self.push_connected_iron_pieces_away(nx, ny)


    def check_win_condition(self):
        """Check if all target positions are occupied by pieces."""
        for (x, y) in self.targets:
            if self.grid[x][y] is None:
                return False
        return True 

