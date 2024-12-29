class Piece:
    def __init__(self, piece_type, position):
        self.piece_type = piece_type 
        self.position = position 

    def __str__(self):
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
        self.grid = [[None for _ in range(size)] for _ in range(size)]  
        self.targets = [tuple(target) for target in targets] if targets else []  
        self.blocks = [tuple(block) for block in blocks] if blocks else []  
        self.pieces = []  

        # Add blocks to the board
        for block in self.blocks:
            self.add_block(block[0], block[1])

        if pieces:
            for piece_data in pieces:
                piece = Piece(piece_data['piece_type'], piece_data['position'])
                self.add_piece(piece, piece_data['position'][0], piece_data['position'][1])

        # for algorithms
        self.states = []
        self.save_state()

        # 
        # in board class
        # 
    def get_grid(self):
            return self.grid
    

    # Adding pieces
    def add_piece(self, piece, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = piece
            self.pieces.append(piece)
        else:
            print("Position is out of the game boundaries")

    def add_block(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[x][y] = 'X'  
        else:
            print("Block position is out of the game boundaries")

    # about the state
    def save_state(self):
        grid_copy = [row[:] for row in self.grid]
        self.states.append(grid_copy)

    def get_state(self):
        grid_state = tuple(
            tuple(str(cell) if cell is not None else "empty" for cell in row)
            for row in self.grid
        )
        pieces_state = tuple(
            sorted((piece.piece_type, tuple(piece.position)) for piece in self.pieces)
        )
        blocks_state = tuple(sorted(self.blocks))  # Include block positions
        targets_state = tuple(sorted(self.targets))  

        return (grid_state, pieces_state, blocks_state, targets_state)


    # Conditions
    def is_within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def can_move_piece(self, x, y, new_x, new_y):
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
        if self.grid[target_x][target_y] == 'X':
            print("Cannot repel due to a block cell.")
            return False
        return True

    def all_targets_filled(self):
        for x, y in self.targets:
            piece = self.grid[x][y]
            if piece is None or not isinstance(piece, Piece):  # if there wasn't a piece, or the piece is not a pice type (I, R, A) => the target is not correct
                return False
        return True

    def check_win_condition(self):
        for (x, y) in self.targets:
            if self.grid[x][y] is None:
                return False
        return True 

    
    # Moving the pieces
    def get_valid_moves_for_piece(self, piece):
        x, y = piece.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        valid_moves = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.can_move_piece(x, y, new_x, new_y):
                valid_moves.append((new_x, new_y))
                print(f"Valid move found for {piece} to ({new_x}, {new_y})")  

        return valid_moves

    def move_piece(self, x, y, new_x, new_y):
        if not self.can_move_piece(x, y, new_x, new_y): 
            # to see if i can move the piece or not
            print("Invalid move.")
            return False

        piece = self.grid[x][y]
        self.grid[x][y] = None
        self.grid[new_x][new_y] = piece # putting the piece in its new position
        piece.position = [new_x, new_y] # making the piece know its new position

        print(f"Piece {piece} moved from ({x}, {y}) to ({new_x}, {new_y})")  # Debugging

        # Apply magnetic effects
        if piece.piece_type == "attractive":
            self.move_adjacent_pieces_towards((new_x, new_y))
        elif piece.piece_type == "repulsive":
            self.move_adjacent_pieces_away((new_x, new_y))

        self.save_state()
        return True
    
    def move_piece_to(self, current_position, new_position):
        if self.is_within_bounds(new_position[0], new_position[1]) and self.grid[new_position[0]][new_position[1]] is None:
            piece = self.grid[current_position[0]][current_position[1]]
            if isinstance(piece, Piece):
                self.grid[current_position[0]][current_position[1]] = None
                piece.position = [new_position[0], new_position[1]]
                self.grid[new_position[0]][new_position[1]] = piece

    def move_adjacent_pieces_towards(self, new_position):
        x, y = new_position

        for j in range(y-1, -1, -1):
            piece = self.grid[x][j]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((x,j), (x,j+1))

        for j in range(y + 1, self.size):
            piece = self.grid[x][j]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((x, j), (x, j-1))

        for i in range(x-1, -1, -1):
            piece = self.grid[i][y]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((i,y), (i+1, y))

        for i in range(x+1, self.size):
            piece = self.grid[i][y]
            if piece != None and isinstance(piece, Piece):
                self.move_piece_to((i, y), (i-1, y))
    
    def move_adjacent_pieces_away(self, new_position):
        directions = ["up", "down", "left", "right"]
        
        for direction in directions:
            x, y = new_position
            
            while True:
                x1, y1 = x, y
                x, y = self.move_position(x, y, direction)

                if not self.is_within_bounds(x, y):
                    break

                if self.grid[x][y] is not None and self.grid[x][y] != 'X': # if there is a piece and that piece is not a block 'X'
                    connected_pieces = self.get_connected_pieces((x1, y1), direction)
                    if connected_pieces:
                        self.move_connected_pieces_away(connected_pieces, direction)
                    break

    def move_position(self, x, y, direction):
        if direction == "up":
            return x - 1, y
        elif direction == "down":
            return x + 1, y
        elif direction == "left":
            return x, y - 1
        elif direction == "right":
            return x, y + 1
        
    def get_connected_pieces(self, start_position, direction):
        connected = []
        x, y = start_position
        
        while True:
            x, y = self.move_position(x, y, direction)

            if not self.is_within_bounds(x, y) or self.grid[x][y] is None:
                break

            connected.append((x, y))
            
        return connected
   
    def move_connected_pieces_away(self, connected_pieces, direction):
        if not connected_pieces:
            return False

        last_piece_pos = connected_pieces[-1]
        lx, ly = last_piece_pos

        # Calculate the position after the last piece
        after_position = self.move_position(lx, ly, direction)

        # Move pieces if possible
        if self.is_within_bounds(after_position[0], after_position[1]) and self.grid[after_position[0]][after_position[1]] is None:
            for pos in reversed(connected_pieces):
                self.move_piece_away(pos, direction)
            return True
        return False

    def move_piece_away(self, current_position, direction):
        cx, cy = current_position
        new_position = self.move_position(cx, cy, direction)

        if self.is_within_bounds(new_position[0], new_position[1]) and self.grid[new_position[0]][new_position[1]] is None:
            piece = self.grid[cx][cy]
            if isinstance(piece, Piece):
                self.grid[cx][cy] = None
                piece.position = [new_position[0], new_position[1]]
                self.grid[new_position[0]][new_position[1]] = piece

    def get_movable_pieces(self):
        movable_pieces = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                piece = self.grid[row][col]
                if isinstance(piece, Piece) and piece.piece_type != "iron":
                    if any(self.can_move_piece(row, col, row + dx, col + dy) 
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                        movable_pieces.append((row, col))
        return movable_pieces

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

