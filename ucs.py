import heapq
import copy


class UCSAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()  # Tracks visited states
        self.board_state_map = {}  # Maps states to board instances

    def solve(self):
        priority_queue = []
        initial_state = self.board.get_state()
        state_costs = {initial_state: 0}

        self.board_state_map[initial_state] = copy.deepcopy(self.board)
        visited = set()

        if self.board.all_targets_filled():
            print("Already solved at the start!")
            return []

        heapq.heappush(priority_queue, (0, 0, initial_state, []))
        visited.add(initial_state)

        while priority_queue:
            _, current_cost, current_state, move_sequence = heapq.heappop(priority_queue)
            
            current_board = self.board_state_map[current_state]

            if current_board.all_targets_filled():
                print("Solution found!")
                return move_sequence

            possible_moves = self.generate_all_possible_moves(current_board)

            for piece, move in possible_moves:
                new_board = copy.deepcopy(current_board)
                
                # Prevent moves into block cells
                if new_board.grid[move[0]][move[1]] == 'X':
                    continue  # Skip blocked paths

                new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_state = new_board.get_state()

                if new_state not in visited:
                    visited.add(new_state)
                    move_cost = 1
                    new_total_cost = current_cost + move_cost

                    self.board_state_map[new_state] = new_board
                    new_move_sequence = move_sequence + [(piece, move)]
                    heapq.heappush(priority_queue, (new_total_cost, new_total_cost, new_state, new_move_sequence))

        print("No solution found.")
        return None


    def generate_all_possible_moves(self, game_instance):
        possible_moves = []
        movable_pieces = game_instance.get_movable_pieces()

        for piece_pos in movable_pieces:
            piece = game_instance.grid[piece_pos[0]][piece_pos[1]]
            valid_moves = game_instance.get_valid_moves_for_piece(piece)
            
            for move in valid_moves:
                possible_moves.append((piece, move))
        
        return possible_moves
