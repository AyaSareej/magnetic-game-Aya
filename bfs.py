import copy
from collections import deque


class BFSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()  # Track visited states
        self.board_state_map = {}  # Map states to board configurations

    def get_state(self):
        """Return a hashable representation of the board state."""
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)

    def solve(self):
        """Perform BFS to find the shortest solution."""
        initial_state = self.get_state()
        self.board_state_map[initial_state] = copy.deepcopy(self.board)
        
        # BFS queue (state, move_sequence)
        queue = deque([(initial_state, [])])
        self.visited.add(initial_state)

        # Early exit if the board is already in a solved state
        if self.board.all_targets_filled():
            print("Already solved at the start!")
            return []

        # BFS Loop
        while queue:
            current_state, move_sequence = queue.popleft()
            current_board = self.board_state_map[current_state]

            # Check if the current board is solved
            if current_board.all_targets_filled():
                print("Solution found!")
                return move_sequence

            # Generate and explore possible moves
            possible_moves = self.generate_all_possible_moves(current_board)

            for piece, move in possible_moves:
                new_board = copy.deepcopy(current_board)
                new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = new_board.get_state()

                # Avoid revisiting states
                if new_state not in self.visited:
                    self.visited.add(new_state)
                    self.board_state_map[new_state] = new_board

                    # Append move and continue BFS
                    new_move_sequence = move_sequence + [(piece, move)]
                    queue.append((new_state, new_move_sequence))

        print("No solution found.")
        return None

    def generate_all_possible_moves(self, game_instance):
        """Generate all possible valid moves for the pieces."""
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  # Skip immovable pieces
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    if game_instance.is_within_bounds(move[0], move[1]) and game_instance.grid[move[0]][move[1]] is None:
                        possible_moves.append((piece, move))
        return possible_moves
