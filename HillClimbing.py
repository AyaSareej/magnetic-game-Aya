import copy
import heapq

class HillClimbingAlgorithm:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def get_state(self):
        board_state = tuple(tuple(cell for cell in row) for row in self.board.get_grid())
        piece_state = tuple(sorted((piece.piece_type, tuple(piece.position)) for piece in self.board.pieces))
        return (board_state, piece_state)

    def heuristic(self, game_instance):
        total_distance = 0
        unfilled_targets = set(game_instance.targets) 

        for piece in game_instance.pieces:
            if piece.piece_type == "iron": 
                continue

            # Calculate the Manhattan distance to each target
            piece_position = piece.position
            distances_to_targets = [(abs(piece_position[0] - tx) + abs(piece_position[1] - ty), (tx, ty))
                                    for tx, ty in unfilled_targets]
            if distances_to_targets:
                min_distance, closest_target = min(distances_to_targets)
                total_distance += min_distance
                unfilled_targets.remove(closest_target)  

        total_distance += len(unfilled_targets) * 10  

        return total_distance

    def solve(self):
        initial_state = self.get_state()
        pq = [(self.heuristic(self.board), self.board, [])]  # Priority queue (heuristic, board, moves)
        self.visited.add(initial_state)

        while pq:
            _, current_game, move_sequence = heapq.heappop(pq)

            if current_game.all_targets_filled():
                return move_sequence

            possible_moves = self.generate_all_possible_moves(current_game)
            best_move = None
            best_heuristic = float('inf')

            for piece, move in possible_moves:
                new_game = copy.deepcopy(current_game)
                new_game.move_piece(piece.position[0], piece.position[1], move[0], move[1])
                new_heuristic = self.heuristic(new_game)

                if new_heuristic < best_heuristic:
                    best_heuristic = new_heuristic
                    best_move = (piece, move)

            if best_move is None:  # No better move found
                print("No progress can be made.")
                return None

            # Apply the best move
            piece, move = best_move
            current_game.move_piece(piece.position[0], piece.position[1], move[0], move[1])
            move_sequence.append((piece, move))
            heapq.heappush(pq, (best_heuristic, current_game, move_sequence))

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
