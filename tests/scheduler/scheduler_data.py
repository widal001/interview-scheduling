INTERVIEWS = {
    "Position 1": ["Alice", "Charlie", "Bob"],
    "Position 2": ["Bob", "Alice", "Charlie"],
    "Position 3": ["Charlie", "Bob", "Alice"],
}

AVAIAILABILITY = {
    "candidates": {
        "Alice": ["9am", "12pm", "3pm"],
        "Bob": ["9am", "12pm", "3pm"],
        "Charlie": ["9am", "12pm", "3pm"],
    },
    "positions": {
        "Position 1": ["9am", "12pm", "3pm"],
        "Position 2": ["9am", "12pm", "3pm"],
        "Position 3": ["9am", "12pm", "3pm"],
    },
}

SCHEDULE = {
    ("Position 1", "Alice"): "9am",
    ("Position 1", "Charlie"): "12pm",
    ("Position 1", "Bob"): "3pm",
    ("Position 2", "Bob"): "9am",
    ("Position 2", "Alice"): "12pm",
    ("Position 2", "Charlie"): "3pm",
    ("Position 3", "Charlie"): "9am",
    ("Position 3", "Bob"): "12pm",
    ("Position 3", "Alice"): "3pm",
}


{
    "s": {
        ("Position 1", "Alice"): 1,
        ("Position 1", "Bob"): 1,
        ("Position 1", "Charlie"): 1,
        ("Position 2", "Alice"): 1,
        ("Position 2", "Bob"): 1,
        ("Position 2", "Charlie"): 1,
        ("Position 3", "Alice"): 1,
        ("Position 3", "Bob"): 1,
        ("Position 3", "Charlie"): 1,
    },
    "t": {},
    ("Alice", "12pm"): {("Position 3", "12pm"): 1},
    ("Alice", "3pm"): {
        ("Position 1", "3pm"): 0,
        ("Position 2", "3pm"): 1,
        ("Position 3", "3pm"): 1,
    },
    ("Alice", "9am"): {
        ("Position 1", "9am"): 0,
        ("Position 2", "9am"): 0,
        ("Position 3", "9am"): 0,
    },
    ("Bob", "12pm"): {
        ("Position 1", "12pm"): 0,
        ("Position 2", "12pm"): 1,
        ("Position 3", "12pm"): 0,
    },
    ("Bob", "3pm"): {
        ("Position 1", "3pm"): 1,
        ("Position 2", "3pm"): 0,
        ("Position 3", "3pm"): 0,
    },
    ("Bob", "9am"): {
        ("Position 1", "9am"): 0,
        ("Position 2", "9am"): 0,
        ("Position 3", "9am"): 1,
    },
    ("Charlie", "12pm"): {
        ("Position 1", "12pm"): 1,
        ("Position 2", "12pm"): 0,
        ("Position 3", "12pm"): 0,
    },
    ("Charlie", "3pm"): {
        ("Position 1", "3pm"): 0,
        ("Position 2", "3pm"): 0,
        ("Position 3", "3pm"): 0,
    },
    ("Charlie", "9am"): {
        ("Position 1", "9am"): 1,
        ("Position 2", "9am"): 1,
        ("Position 3", "9am"): 0,
    },
    ("Position 1", "12pm"): {"t": 1},
    ("Position 1", "3pm"): {"t": 1},
    ("Position 1", "9am"): {"t": 1},
    ("Position 1", "Alice"): {
        ("Alice", "12pm"): 0,
        ("Alice", "3pm"): 1,
        ("Alice", "9am"): 0,
    },
    ("Position 1", "Bob"): {("Bob", "12pm"): 0, ("Bob", "3pm"): 1, ("Bob", "9am"): 0},
    ("Position 1", "Charlie"): {
        ("Charlie", "12pm"): 1,
        ("Charlie", "3pm"): 0,
        ("Charlie", "9am"): 0,
    },
    ("Position 2", "12pm"): {"t": 1},
    ("Position 2", "3pm"): {"t": 1},
    ("Position 2", "9am"): {"t": 1},
    ("Position 2", "Alice"): {
        ("Alice", "12pm"): 1,
        ("Alice", "3pm"): 0,
        ("Alice", "9am"): 0,
    },
    ("Position 2", "Bob"): {("Bob", "12pm"): 1, ("Bob", "3pm"): 0, ("Bob", "9am"): 0},
    ("Position 2", "Charlie"): {
        ("Charlie", "12pm"): 0,
        ("Charlie", "3pm"): 0,
        ("Charlie", "9am"): 1,
    },
    ("Position 3", "12pm"): {"t": 1},
    ("Position 3", "3pm"): {"t": 1},
    ("Position 3", "9am"): {"t": 1},
    ("Position 3", "Alice"): {
        ("Alice", "12pm"): 0,
        ("Alice", "3pm"): 1,
        ("Alice", "9am"): 0,
    },
    ("Position 3", "Bob"): {("Bob", "12pm"): 0, ("Bob", "3pm"): 0, ("Bob", "9am"): 1},
    ("Position 3", "Charlie"): {
        ("Charlie", "12pm"): 0,
        ("Charlie", "3pm"): 0,
        ("Charlie", "9am"): 1,
    },
}
