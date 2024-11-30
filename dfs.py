import copy

class DFSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def get_state(self, game_instance):
        """Returns a hashable representation of the current game state."""
        board_state = tuple(tuple(cell for cell in row) for row in game_instance.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in game_instance.pieces))
        return (board_state, piece_state)


    def solve(self):
        """Solve the game using DFS."""
        initial_state = self.get_state(self.board)
        stack = [(self.board, [], initial_state)]  # Stack holds (board state, move sequence, state hash)
        self.visited.add(initial_state)

        print(f"Initial State: {initial_state}")  # Debugging output

        while stack:
            current_game, move_sequence, current_state = stack.pop()

            # Check if the current state is the solution
            if current_game.all_targets_filled():
                print("Solution found!")
                return move_sequence

            # Generate possible moves
            possible_moves = self.generate_all_possible_moves(current_game)
            print(f"Possible moves: {[(piece, move) for piece, move in possible_moves]}")  # Debugging output

            for piece, move in possible_moves:
                new_game = copy.deepcopy(current_game)
                new_game.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = self.get_state(new_game)

                print(f"New state generated: {new_state}")  # Debugging output

                if new_state not in self.visited:
                    self.visited.add(new_state)
                    stack.append((new_game, move_sequence + [(piece, move)], new_state))
                else:
                    print(f"State already visited: {new_state}")  # Debugging output

        print("No solution found.")
        return None  # No solution found

    
    def generate_all_possible_moves(self, game_instance):
        """Generate all valid moves for all movable pieces."""
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  # Iron pieces cannot be moved manually
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    if (
                        game_instance.is_within_bounds(move[0], move[1])
                        and game_instance.grid[move[0]][move[1]] is None
                    ):
                        possible_moves.append((piece, move))
        return possible_moves

