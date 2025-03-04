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


def computer_guess(board, previous_hits=None):
    if previous_hits:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = previous_hits[0] + dr, previous_hits[1] + dc
            if 0 <= new_row < 9 and 0 <= new_col < 9:
                if board[new_row][new_col] == ' ':
                    return new_row, new_col
    while True:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] == ' ':
            return row, col

def is_ship_sunk(ship_positions, board, ship):
    """
    Checks if all parts of the specified ship are hit ('X').
    """
    return all(board[row][col] == 'X' for row, col in ship_positions[ship])

def play_game():
    """
    This function is the main game loop where the player and
    computer take turns guessing each other's ships.
    It displays the player's board, the computer's board,
    and prompts the player to enter a guess.
    The player can enter 'exit' to quit the game at any time.
    The game continues until all the ships of either
    the player or the computer have been sunk.
    It also keeps track of the number of guesses made by the player
    and the computer.
    """

    time.sleep(1)

    # Validate name input
    name = input('Enter your name: ')
    while not validate_name(name):
        print('Invalid name. Please enter a valid name.')
        name = input('Enter your name: ')
        time.sleep(1)

    time.sleep(1)
    input('Press Enter to start the game...')

    global ships
    player_board = create_board()
    computer_board = create_board()

    print('Placing ships on the board... 🌊 🌊 🌊 🌊 🌊')
    time.sleep(1)

    player_ship_positions = place_ships(player_board)
    computer_ship_positions = place_ships(computer_board)
    player_ships_sunk = {ship: False for ship in ships}
    computer_ships_sunk = {ship: False for ship in ships}
    guesses = 0
    # Set to store guessed coordinates
    guessed_coords = set()

    print('Player Board:')
    print_board(player_board)

    while True:
        guess = input('Enter your guess (e.g. A1), or type "exit" to quit: ')
        time.sleep(1)

        # Check if the player wants to exit
        if guess.lower() == 'exit':
            print('Quitting the game...Traitor!😈')
            return name
        time.sleep(1)

        # Check if guess is valid
        if not validate_input(guess, computer_board):
            print('Invalid input. Please enter a valid guess. 💀')
            continue
        time.sleep(1)

        # Check if guess has already been made
        col = guess[0].upper()
        row = int(guess[1:]) - 1
        if (row, ord(col) - ord('A')) in guessed_coords:
            print('You have already guessed that coordinate. Try again. ⛔')
            continue
        time.sleep(1)

        # Add current guess to guessed coordinates
        guessed_coords.add((row, ord(col) - ord('A')))

        # Process the guess
        # Now guessing on computer's board
        if computer_board[row][ord(col) - ord('A')] == 'O':
            computer_board[row][ord(col) - ord('A')] = 'X'
            print(f'{name} Hit an enemy ship! 🎯')
            # Add delay for dramatic effect
            time.sleep(1)

            # Check if a ship has been sunk
            for ship in ships:
                if is_ship_sunk(computer_ship_positions, computer_board, ship):
                    if not computer_ships_sunk[ship]:
                        print(f'{name} sunk the enemy\'s {ship}! 🚩')
                        computer_ships_sunk[ship] = True
                        time.sleep(1)

        else:
            computer_board[row][ord(col) - ord('A')] = 'M'
            print(f'{name} missed enemy ship🌊 🚫')
            time.sleep(1)

        guesses += 1
        if all(computer_ships_sunk.values()):
            print('Victory! You sunk all the enemy\'s ships. You win! 🏆')
            print(f'Total Guesses: {guesses}')
            break
        time.sleep(1)

        # Now computer guesses on player's board
        computer_row, computer_col = computer_guess(player_board)

        # Now guessing on player's board
        if player_board[computer_row][computer_col] == 'O':
            player_board[computer_row][computer_col] = 'X'
            print('Enemy hit your ship! 💥')

            # Add delay for dramatic effect
            time.sleep(1)

            # Check if a ship has been sunk
            for ship in ships:
                if is_ship_sunk(player_ship_positions, player_board, ship):
                    if not player_ships_sunk[ship]:
                        print(f'The enemy sunk your {ship}! 💣')
                        player_ships_sunk[ship] = True
                        time.sleep(1)

        else:
            player_board[computer_row][computer_col] = 'M'
            print('Enemy missed your ship! 🚫')
            time.sleep(1)
            print("Enemy guessed: "
                  f"{chr(computer_col + ord('A'))}{computer_row + 1}")
            time.sleep(1)

        guesses += 1
        if all(player_ships_sunk.values()):
            print('Defeat! The enemy sunk all your ships. You lose. 😭')
            time.sleep(1)
            print(f'Total Guesses: {guesses}')
            time.sleep(1)
            break
        print('Player Board:')
        print_board(player_board)
        print('Computer Board:')
        print_board(computer_board, hide_ships=True)

        time.sleep(1)

    return name


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
    play_game()
    print('Thanks for playing Battleship! 👋')


if __name__ == '__main__':
    main()
