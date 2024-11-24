from collections import deque
import copy
from search_strategy import SearchStrategy

import copy

class DFS(SearchStrategy):
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def solve(self):
        
        if current_game.all_targets_filled():
            return []  

        self.visited.clear()  
        max_depth = 15 
        return self.dfs(self.board, [], 0, max_depth)

    def dfs(self, current_game, move_sequence, depth, max_depth):
        if depth > max_depth:
            
            return None
        
        current_state = self.get_state(current_game)
        if current_state in self.visited:
            
            return None

        self.visited.add(current_state)

        if current_game.board.all_targets_filled():
            # print(move_sequence)
            return move_sequence

        possible_moves = self.generate_all_possible_moves(current_game)

        for move in possible_moves:
            new_game = copy.deepcopy(current_game)  
            new_game.make_move(move)

            
            solution = self.dfs(new_game, move_sequence + [move], depth + 1, max_depth)
            if solution:
                return solution  

        return None  