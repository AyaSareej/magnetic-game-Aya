from game import Game

levels_data = [
    {
        "board_size": 4,
        "target_cells": [[1, 1], [1, 3]],
        "block_cells": [],
        "pieces": [
            {"piece_type": "repulsive", "position": [3, 0]},
            {"piece_type": "iron", "position": [1, 2]}
        ]
    },
    {
        "board_size": 4,
        "target_cells": [[1, 0], [1, 2], [2, 1], [2, 2]],
        "block_cells": [],
        "pieces": [
            {"piece_type": "attractive", "position": [3, 3]},
            {"piece_type": "iron", "position": [0, 3]},
            {"piece_type": "iron", "position": [2, 0]},
            {"piece_type": "iron", "position": [3, 0]}
        ]
    },
    {
        "board_size": 4,
        "target_cells": [[0, 0], [0, 2], [2, 2]],
        "block_cells": [[0, 3], [1, 3], [2, 3], [3, 3]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 0]},
            {"piece_type": "iron", "position": [1, 1]},
            {"piece_type": "iron", "position": [1, 2]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 0], [0, 2], [1, 4], [2, 4]],
        "block_cells": [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4]],
        "pieces": [
            {"piece_type": "attractive", "position": [2, 2]},
            {"piece_type": "iron", "position": [0, 1]},
            {"piece_type": "iron", "position": [0, 3]},
            {"piece_type": "repulsive", "position": [1, 2]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 1], [0, 3], [0, 2]],
        "block_cells": [[1, 0], [1, 1], [1, 3], [1, 4], [2, 2]],
        "pieces": [
            {"piece_type": "attractive", "position": [1, 2]},
            {"piece_type": "iron", "position": [0, 0]},
            {"piece_type": "iron", "position": [0, 4]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[2, 0], [1, 0], [4, 0], [4, 2]],
        "block_cells": [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [0, 2], [0, 3], [1, 2], [1, 3]],
        "pieces": [
            {"piece_type": "attractive", "position": [3, 1]},
            {"piece_type": "iron", "position": [0, 0]},
            {"piece_type": "iron", "position": [1, 0]},
            {"piece_type": "iron", "position": [4, 3]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 2], [1, 3], [4, 4]],
        "block_cells": [[2, 2], [3, 3], [3, 0]],
        "pieces": [
            {"piece_type": "attractive", "position": [0, 0]},
            {"piece_type": "attractive", "position": [0, 4]},
            {"piece_type": "repulsive", "position": [1, 1]},
            {"piece_type": "repulsive", "position": [1, 2]},
            {"piece_type": "iron", "position": [2, 1]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 3], [1, 2], [2, 3]],
        "block_cells": [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 0]},
            {"piece_type": "iron", "position": [1, 1]},
            {"piece_type": "iron", "position": [1, 3]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 0], [2, 3], [4, 4]],
        "block_cells": [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [4, 0], [4, 1], [4, 2]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 1]},
            {"piece_type": "iron", "position": [1, 0]},
            {"piece_type": "iron", "position": [2, 0]},
            {"piece_type": "iron", "position": [3, 1]},
            {"piece_type": "iron", "position": [3, 2]}
        ]
    },
    {
        "board_size": 6,
        "target_cells": [[0, 3], [1, 1], [2, 1]],
        "block_cells": [[1, 0], [2, 0], [1, 4], [1, 5], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5]],
        "pieces": [
            {"piece_type": "attractive", "position": [2, 3]},
            {"piece_type": "iron", "position": [0, 0]},
            {"piece_type": "iron", "position": [0, 4]},
            {"piece_type": "iron", "position": [0, 5]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 3], [1, 2], [2, 3]],
        "block_cells": [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 0]},
            {"piece_type": "iron", "position": [1, 1]},
            {"piece_type": "iron", "position": [1, 3]}
        ]
    },
    {
        "board_size": 7,
        "target_cells": [[0, 1], [0, 6]],
        "block_cells": [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]],
        "pieces": [
            {"piece_type": "repulsive", "position": [0, 0]},
            {"piece_type": "iron", "position": [0, 3]},
            {"piece_type": "iron", "position": [0, 5]}
        ]
    },
    {
        "board_size": 5,
        "target_cells": [[0, 3], [1, 2], [2, 3]],
        "block_cells": [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]],
        "pieces": [
            {"piece_type": "repulsive", "position": [2, 0]},
            {"piece_type": "iron", "position": [1, 1]},
            {"piece_type": "iron", "position": [1, 3]}
        ]
    }
]


if __name__ == "__main__":
    game = Game(levels_data)
    game.choose_level()
