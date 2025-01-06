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

def print_board(board, hide_ships=False):
    """
    Prints the board with row numbers and column letters.
    Optionally hides ships ('O') if hide_ships is True.
    """
    symbols = {' ': '⬜', 'O': '🚢', 'X': '🔥', 'M': '🌊'}
    print('   A B C D E F G H I')
    print('  -------------------')
    for i in range(9):
        row = [symbols[cell] if not (hide_ships and cell == 'O') else symbols[' '] for cell in board[i]]
        print(f'{i + 1} |' + '|'.join(row) + '|')
        print('  -------------------')
