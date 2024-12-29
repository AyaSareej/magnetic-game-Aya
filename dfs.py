import copy


class DFSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()  
        self.board_state_map = {}  # Store state-to-board mapping for backtracking

    def get_state(self):
        """Return a hashable state representation of the board."""
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)

    def solve(self):
        """Perform DFS to solve the game."""
        initial_state = self.get_state()
        self.board_state_map[initial_state] = copy.deepcopy(self.board)
        stack = [(initial_state, [])]  # (state, move_sequence)
        self.visited.add(initial_state)

        # Early exit if the board is already in a solved state
        if self.board.all_targets_filled():
            print("Already solved at the start!")
            return []

        while stack:
            current_state, move_sequence = stack.pop()
            current_board = self.board_state_map[current_state]

            if current_board.all_targets_filled():
                print("Solution found!")
                return move_sequence

            # Generate possible moves
            possible_moves = self.generate_all_possible_moves(current_board)

            for piece, move in possible_moves:
                new_board = copy.deepcopy(current_board)
                new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = new_board.get_state()

                if new_state not in self.visited:
                    self.visited.add(new_state)
                    self.board_state_map[new_state] = new_board

                    # Append move to the sequence and continue DFS
                    new_move_sequence = move_sequence + [(piece, move)]
                    stack.append((new_state, new_move_sequence))

        print("No solution found.")
        return None

    def generate_all_possible_moves(self, game_instance):
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  # Skip immovable iron pieces
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    if game_instance.is_within_bounds(move[0], move[1]) and game_instance.grid[move[0]][move[1]] is None:
                        possible_moves.append((piece, move))
        return possible_moves
