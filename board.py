from collections import deque


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


        # 
        # BFS
        # 

    def bfs_solve(self):
            """Solve the game using BFS and return the sequence of moves."""
            initial_state = self.get_state()
            queue = deque([(initial_state, [])])  # (state, moves)
            visited = set()
            visited.add(initial_state)

            while queue:
                current_state, moves = queue.popleft()
                self.set_state(current_state)

                if self.check_win_condition():
                    return moves  # Return the sequence of moves leading to the solution

                # Generate all possible moves from the current state
                for piece, valid_moves in self.get_all_valid_moves().items():
                    for move in valid_moves:
                        new_state = self.simulate_move(piece, move)
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, moves + [(piece, move)]))

            return None  # No solution found

    def get_state(self):
        """Get a tuple representing the current state of the board."""
        return tuple((piece.piece_type, tuple(piece.position)) for piece in self.pieces)

    def set_state(self, state):
        """Set the board to a specific state."""
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.pieces = []
        for piece_type, position in state:
            piece = Piece(piece_type, list(position))
            self.add_piece(piece, position[0], position[1])

    def get_all_valid_moves(self):
        """Get all valid moves for all pieces."""
        valid_moves = {}
        for piece in self.pieces:
            if piece.piece_type == "iron":  # Iron pieces cannot be moved manually
                continue
            valid_moves[piece] = self.get_valid_moves_for_piece(piece)
        return valid_moves

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

    def simulate_move(self, piece, move):
        """Simulate a move and return the resulting state."""
        x, y = piece.position
        new_x, new_y = move
        self.move_piece(x, y, new_x, new_y)
        return self.get_state()



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
        else:
            print("Block position is out of the game boundaries")

    def display_board(self):
        """Display the grid state for the user, marking targets with 'T' if empty."""
        print("Grid game state:")
        print("    " + "  ".join([str(i) for i in range(self.size)]))
        print(" +" + "---" * self.size + "+")

        for i, row in enumerate(self.grid):
            row_display = f"{i}| "
            for j, cell in enumerate(row):
                if cell is None:
                    row_display += " T " if (i, j) in self.targets else " . "
                elif cell == 'X':
                    row_display += " X "  # Display block as 'X'
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

