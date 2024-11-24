import heapq
import copy

class UCSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def get_state(self):
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)

    def solve(self):
        priority_queue = []
        initial_state = self.get_state()

        state_costs = {initial_state: 0}  

        if self.board.all_targets_filled():
            return []  # No moves needed; already solved

        heapq.heappush(priority_queue, (0, self.board, []))  # Cost, Board, Move Sequence
        self.visited.clear()
        self.visited.add(initial_state)

        while priority_queue:
            current_cost, current_board, move_sequence = heapq.heappop(priority_queue)

            # If the game is already solved, return the move sequence
            if current_board.all_targets_filled():
                return move_sequence

            # Generate possible moves
            possible_moves = self.generate_all_possible_moves(current_board)

            for piece, move in possible_moves:
                # Create a new game state by applying the move
                new_board = copy.deepcopy(current_board)
                new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = new_board.get_state()

                # Calculate the cost
                move_cost = self.get_move_cost(piece, move)

                # If this state has not been visited or a lower-cost path is found
                if new_state not in self.visited:
                    self.visited.add(new_state)
                    new_cost = current_cost + move_cost
                    heapq.heappush(priority_queue, (new_cost, new_board, move_sequence + [(piece, move)]))

        print("No solution found.")  # If queue is empty and no solution
        return None  


    def generate_all_possible_moves(self, game_instance):
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron": 
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    # Ensure target cell is empty and doesn't collide with blocks
                    if game_instance.grid[move[0]][move[1]] is None:
                        possible_moves.append((piece, move))
        print(f"Generated Possible Moves: {possible_moves}")  # Debugging
        return possible_moves



    def get_move_cost(self, piece, target_position):
        """
        1 for every move
        """
        return 1
        # current_x, current_y = piece.position
        # target_x, target_y = target_position
        # return abs(current_x - target_x) + abs(current_y - target_y)  

