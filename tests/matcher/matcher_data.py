PREFS = {
    "complete": {
        "candidates": {
            "Alice": {"Position 1": 1, "Position 2": 2, "Position 3": 3},
            "Bob": {"Position 1": 3, "Position 2": 1, "Position 3": 2},
            "Charlie": {"Position 1": 2, "Position 2": 3, "Position 3": 1},
        },
        "positions": {
            "Position 1": {"Alice": 1, "Bob": 3, "Charlie": 2},
            "Position 2": {"Alice": 2, "Bob": 1, "Charlie": 3},
            "Position 3": {"Alice": 3, "Bob": 2, "Charlie": 1},
        },
    },
    "match swapping": {
        "candidates": {
            "Alice": {"Position 1": 1, "Position 2": 2, "Position 3": 3},
            "Bob": {"Position 1": 1, "Position 2": 2, "Position 3": 3},
            "Charlie": {"Position 1": 1, "Position 2": 2, "Position 3": 3},
        },
        "positions": {
            "Position 1": {"Alice": 3, "Bob": 2, "Charlie": 1},
            "Position 2": {"Alice": 3, "Bob": 2, "Charlie": 1},
            "Position 3": {"Alice": 3, "Bob": 2, "Charlie": 1},
        },
    },
}

INTERVIEWS = {
    "complete": {
        "candidates": {
            "Alice": ["Position 1", "Position 2", "Position 3"],
            "Bob": ["Position 2", "Position 3", "Position 1"],
            "Charlie": ["Position 3", "Position 1", "Position 2"],
        },
        "positions": {
            "Position 1": ["Alice", "Charlie", "Bob"],
            "Position 2": ["Bob", "Alice", "Charlie"],
            "Position 3": ["Charlie", "Bob", "Alice"],
        },
    },
    "match swapping": {
        "candidates": {
            "Alice": ["Position 3"],
            "Bob": ["Position 1", "Position 2"],
            "Charlie": ["Position 1", "Position 2"],
        },
        "positions": {
            "Position 1": ["Charlie", "Bob"],
            "Position 2": ["Charlie", "Bob"],
            "Position 3": ["Alice"],
        },
    },
}
