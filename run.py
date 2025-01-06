import random
import re
import time

# Define ships globally
ships = {
    'Carrier': 5,
    'Battleship': 4,
    'Cruiser': 3,
    'Submarine': 3,
    'Destroyer': 2
}

def create_board():
    """
    Creates a 9x9 empty board initialized with ' '.
    """
    return [[' '] * 9 for _ in range(9)]