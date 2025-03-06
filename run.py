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
        row = [
            symbols[cell] if not (hide_ships and cell == 'O')
            else symbols[' '] for cell in board[i]
            ]
        print(f'{i + 1} |' + '|'.join(row) + '|')
        print('  -------------------')


def place_ships(board):
    """
    Randomly places ships on the board.
    Ensures ships do not overlap or touch each other.
    """
    def is_valid_placement(row, col, size, orientation):
        if orientation == 'horizontal':
            if col + size > 9 or any(
                board[row][col + i] != ' ' for i in range(size)
            ):
                return False
        else:
            if row + size > 9 or any(
                board[row + i][col] != ' ' for i in range(size)
            ):
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


def validate_input(guess):
    """
    Validates user input for the guess.
    """
    msg_invalid = "Invalid input format. Use a letter (A-I) and number (1-9)."
    if len(guess) < 2 or len(guess) > 3:
        print(msg_invalid)
        return False
    col, row = guess[0].upper(), guess[1:]
    if col not in 'ABCDEFGHI' or not row.isdigit() or not (1 <= int(row) <= 9):
        print("Invalid coordinates. Column must be A-I, and row must be 1-9.")
        return False
    return True


def computer_guess(board, last_hit=None):
    """
    Computer guesses intelligently based on previous hits.
    If last_hit is provided, it will target adjacent cells.
    If no last hit, it will choose a random empty cell.
    """
    def adjacent_cells(row, col):
        """Returns a list of valid adjacent cells (up, down, left, right)."""
        adjacent = []
        if row > 0: adjacent.append((row - 1, col))  # Up
        if row < 8: adjacent.append((row + 1, col))  # Down
        if col > 0: adjacent.append((row, col - 1))  # Left
        if col < 8: adjacent.append((row, col + 1))  # Right
        return adjacent

    # If there's a last hit, try surrounding cells first
    if last_hit:
        row, col = last_hit
        possible_moves = adjacent_cells(row, col)
        # Filter out moves that are either already hit or missed
        possible_moves = [
            (r, c) for (r, c) in possible_moves if board[r][c] == ' '
        ]
        if possible_moves:
            # Choose a random valid adjacent cell
            row, col = random.choice(possible_moves)
        else:
            # If no valid adjacent cells, pick a random empty space
            while True:
                row, col = random.randint(0, 8), random.randint(0, 8)
                if board[row][col] == ' ':
                    break
    else:
        # If no hits yet, guess randomly
        while True:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] == ' ':
                break

    # Return the guess (row, col)
    return row, col


def is_ship_sunk(ship_positions, board, ship):
    """
    Checks if all parts of the specified ship are hit ('X').
    """
    return all(board[row][col] == 'X' for row, col in ship_positions[ship])


def play_game():
    """
    Main game loop where player and computer alternate turns.
    """
    name = input('Enter your name: ').strip()
    while not name or re.match(r'^\d', name):
        print('Invalid name. Please enter a valid name.')
        name = input('Enter your name: ').strip()

    input('Press Enter to start the game...')

    player_board = create_board()
    computer_board = create_board()

    print('Placing ships on the boards... 🌊')
    time.sleep(1)
    player_ship_positions = place_ships(player_board)
    computer_ship_positions = place_ships(computer_board)
    player_ships_sunk = {ship: False for ship in ships}
    computer_ships_sunk = {ship: False for ship in ships}
    guessed_coords = set()
    last_hit = None

    print('Player Board:')
    print_board(player_board)
    time.sleep(1)

    while True:
        guess = input('Enter your guess, or type "exit" to quit: ').strip()

        if guess.lower() == 'exit':
            print('Quitting the game... Goodbye! 👋')
            break

        if not validate_input(guess):
            continue

        col = ord(guess[0].upper()) - ord('A')
        row = int(guess[1:]) - 1

        if (row, col) in guessed_coords:
            print('You have already guessed that coordinate. Try again. ⛔')
            continue

        guessed_coords.add((row, col))

        if computer_board[row][col] == 'O':
            computer_board[row][col] = 'X'
            print('Hit! 🎯')
            time.sleep(1)
            for ship in ships:
                if is_ship_sunk(computer_ship_positions, computer_board, ship):
                    if not computer_ships_sunk[ship]:
                        print(f"You sunk the enemy's {ship}! 🚩")
                        computer_ships_sunk[ship] = True
        else:
            computer_board[row][col] = 'M'
            print('Miss! 🌊')
            time.sleep(1)

        if all(computer_ships_sunk.values()):
            print("Victory! You sunk all the enemy's ships! 🏆")
            break

        computer_row, computer_col = computer_guess(player_board, last_hit)

        if player_board[computer_row][computer_col] == 'O':
            player_board[computer_row][computer_col] = 'X'
            print('Enemy hit your ship! 💥')
            time.sleep(1)
            last_hit = (computer_row, computer_col)
            for ship in ships:
                if is_ship_sunk(player_ship_positions, player_board, ship):
                    if not player_ships_sunk[ship]:
                        print(f'The enemy sunk your {ship}! 💣')
                        player_ships_sunk[ship] = True
        else:
            player_board[computer_row][computer_col] = 'M'
            print(f'Enemy missed! 🌊 (Enemy guessed {chr(computer_col + ord("A"))}{computer_row + 1})')
            last_hit = None
            time.sleep(1)

        if all(player_ships_sunk.values()):
            print('Defeat! The enemy sunk all your ships! 😭')
            break

        print('Player Board:')
        print_board(player_board)
        time.sleep(1)
        print('Computer Board:')
        print_board(computer_board, hide_ships=True)
        time.sleep(1)


def main():
    """
    Entry point of the program.
    """
    print("Welcome to Battleship! 🚢")
    print("""
    Instructions:
    1. Enter your name when prompted.
    2. The game will create a 9x9 board for you and the computer.
    3. Ships will be placed randomly on the board.
    4. Guess the position of the enemy ships by entering coordinates (e.g. A1).
    5. The computer will tell you if your guess was a hit or a miss.
    6. The computer will also guess the location of your ships.
    7. The first to sink all the opponent's ships wins the game.
    8. You can exit the game at any time by typing 'exit' during your turn.
    Have fun playing Battleship! 🎮
    """)
    time.sleep(1)
    player_name = play_game()
    time.sleep(1)
    print(f'Thanks for playing! Goodbye, {player_name}! 👋')


if __name__ == '__main__':
    main()
