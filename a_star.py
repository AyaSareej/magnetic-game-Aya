import heapq
import copy

class AStarAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()
        self.board_state_map = {}  
    
    def heuristic(self, board):
        total_distance = 0
        unfilled_targets = set(board.targets)

        for piece in board.pieces:
            if piece.piece_type == "iron":
                continue

            piece_position = piece.position
            distances = [
                abs(piece_position[0] - tx) + abs(piece_position[1] - ty)
                for tx, ty in unfilled_targets
            ]

            if distances:
                min_distance = min(distances)
                total_distance += min_distance
                
                block_penalty = sum(
                    10 for block in board.blocks
                    if abs(block[0] - piece_position[0]) + abs(block[1] - piece_position[1]) == 1
                )
                total_distance += block_penalty

        return total_distance


    def solve(self):
        priority_queue = []
        initial_state = self.board.get_state() 
        state_costs = {initial_state: 0}  # g(n)

        self.board_state_map[initial_state] = copy.deepcopy(self.board)
        
        if self.board.all_targets_filled():
            print("Already solved at the start!")
            return []

        # A* starts with (f-cost, g-cost, state, move_sequence)
        heapq.heappush(priority_queue, (self.heuristic(self.board), 0, initial_state, []))
        self.visited.add(initial_state)

        while priority_queue:
            f_cost, g_cost, current_state, move_sequence = heapq.heappop(priority_queue)
            
            current_board = self.board_state_map[current_state]

            if current_board.all_targets_filled():
                print("Solution found!")
                return move_sequence

            possible_moves = self.generate_all_possible_moves(current_board)
            
            for piece, move in possible_moves:
                new_board = copy.deepcopy(current_board)
                if new_board.move_piece(piece.position[0], piece.position[1], move[0], move[1]):
                    new_state = new_board.get_state()
                    move_cost = 1  # g cost increment
                    new_g_cost = g_cost + move_cost
                    new_h_cost = self.heuristic(new_board)
                    new_f_cost = new_g_cost + new_h_cost

                    if new_state not in self.visited or state_costs.get(new_state, float('inf')) > new_g_cost:
                        self.visited.add(new_state)
                        state_costs[new_state] = new_g_cost
                        self.board_state_map[new_state] = new_board
                        
                        new_move_sequence = move_sequence + [(piece, move)]  
                        heapq.heappush(priority_queue, (new_f_cost, new_g_cost, new_state, new_move_sequence))

        print("No solution found.")
        return None

    def generate_all_possible_moves(self, game_instance):
        possible_moves = []
        for piece in game_instance.pieces:
            if piece.piece_type != "iron":  
                valid_moves = game_instance.get_valid_moves_for_piece(piece)
                for move in valid_moves:
                    possible_moves.append((piece, move))
        return possible_moves
