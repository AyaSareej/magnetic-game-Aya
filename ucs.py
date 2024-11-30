import heapq
import copy

class UCSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def get_state(self):
        """
        Returns a hashable state representation of the board.
        Includes grid and pieces.
        """
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)

    def get_move_cost(self, piece, move):
        """
        Calculate the cost of a move.
        In this case, the cost is always 1.
        """
        return 1

    def solve(self):
        """
        Solve the game using UCS (Uniform Cost Search).
        """
        priority_queue = []
        initial_state = self.get_state()
        state_costs = {initial_state: 0}

        if self.board.all_targets_filled():
            print("Already solved at the start!")
            return []  # Already solved, no moves needed

        # Initialize the priority queue
        heapq.heappush(priority_queue, (0, initial_state, []))  # Cost, State, Move Sequence
        self.visited.add(initial_state)

        while priority_queue:
            current_cost, current_state, move_sequence = heapq.heappop(priority_queue)

            # Restore the board state
            board_state, piece_state = current_state
            self.board.set_state((board_state, piece_state))

            print(f"Exploring state with cost {current_cost}. Move sequence: {move_sequence}")

            # Check for solution
            if self.board.all_targets_filled():
                print("Solution found!")
                return move_sequence

            # Generate possible moves
            possible_moves = self.generate_all_possible_moves(self.board)

            for piece, move in possible_moves:
                new_board = copy.deepcopy(self.board)
                if new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1]):
                    new_state = self.get_state()
                    move_cost = self.get_move_cost(piece, move)
                    new_total_cost = current_cost + move_cost

                    # Debugging output for move evaluation
                    print(f"Evaluating move: {piece} to {move}. Total cost: {new_total_cost}")

                    if new_state not in self.visited or state_costs.get(new_state, float('inf')) > new_total_cost:
                        self.visited.add(new_state)
                        state_costs[new_state] = new_total_cost
                        heapq.heappush(priority_queue, (new_total_cost, new_state, move_sequence + [(piece, move)]))

            # Debugging output for priority queue
            print(f"Priority queue length: {len(priority_queue)}")

        print("No solution found.")
        return None

    def generate_all_possible_moves(self, game_instance):
        """
        Generate all valid moves for all movable pieces on the board.
        """
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  # Skip iron pieces, as they are immovable
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    if game_instance.is_within_bounds(move[0], move[1]) and game_instance.grid[move[0]][move[1]] is None:
                        possible_moves.append((piece, move))
        print(f"Generated possible moves: {[(p.piece_type, m) for p, m in possible_moves]}")  # Debugging output
        return possible_moves
