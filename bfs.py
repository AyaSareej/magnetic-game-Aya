from collections import deque
import copy 

class BFSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def get_state(self):
        """Returns a hashable representation of the current game state."""
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)



    def solve(self):
        """Solve the game using BFS."""
        initial_state = self.get_state()
        queue = deque([(self.board, [])])  # Queue holds (state, moves)
        self.visited.add(initial_state)

        print(f"Initial State: {initial_state}")  # Debugging

        while queue:
            current_game, move_sequence = queue.popleft()
            # print(f"Exploring State: {self.get_state()}, Moves: {move_sequence}")  # Debugging

            if current_game.all_targets_filled():
                return move_sequence

            possible_moves = self.generate_all_possible_moves(current_game)
            for piece, move in possible_moves:
                new_game = copy.deepcopy(current_game)
                new_game.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = tuple(tuple(row) for row in new_game.get_grid())
                if new_game.all_targets_filled():
                    return move_sequence + [(piece, move)]

                if new_state not in self.visited:
                    self.visited.add(new_state)
                    queue.append((new_game, move_sequence + [(piece, move)]))

        print("No solution found.")
        return None  # No solution found

    
    def generate_all_possible_moves(self, game_instance):
        """Generate all valid moves for all movable pieces."""
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  # Iron pieces cannot be moved manually
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    possible_moves.append((piece, move))
        return possible_moves

