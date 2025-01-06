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

def place_ships(board):
    """
    Randomly places ships on the board.
    Ensures ships do not overlap or touch each other.
    """
    def is_valid_placement(row, col, size, orientation):
        if orientation == 'horizontal':
            if col + size > 9 or any(board[row][col + i] != ' ' for i in range(size)):
                return False
        else:
            if row + size > 9 or any(board[row + i][col] != ' ' for i in range(size)):
                return False
        return True

    def mark_ship(row, col, size, orientation):
        positions = []
        for i in range(size):
            if orientation == 'horizontal':
                board[row][col + i] = 'O'
                positions.append((row, col + i))
            else:
                board[row + i][col] = 'O'
                positions.append((row + i, col))
        return positions

    ship_positions = {}
    for ship, size in ships.items():
        placed = False
        while not placed:
            orientation = random.choice(['horizontal', 'vertical'])
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if is_valid_placement(row, col, size, orientation):
                ship_positions[ship] = mark_ship(row, col, size, orientation)
                placed = True
    return ship_positions
