import random
import re
import time
import emoji

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
    This function creates a 9x9 empty board with all cells initialized to ' '.
    """
    board = []
    for _ in range(9):
        row = [' '] * 9
        board.append(row)
    return board


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
    This function randomly places the ships on the board.
    It checks if the ship can be placed in the specified orientation
    (horizontal or vertical) without overlapping with other ships
    or going out of bounds.
    If the ship can be placed, it updates the board with
    the ship's position.
    The function continues to place ships until all ships
    have been placed successfully.
    """
    global ships
    ship_positions = {ship: [] for ship in ships}
    for ship, size in ships.items():
        placed = False
        while not placed:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, 8)
                col = random.randint(0, 9 - size)
                if all(board[row][col + i] == ' ' for i in range(size)):
                    for i in range(size):
                        board[row][col + i] = 'O'
                        ship_positions[ship].append((row, col + i))
                    placed = True
            else:
                row = random.randint(0, 9 - size)
                col = random.randint(0, 8)
                if all(board[row + i][col] == ' ' for i in range(size)):
                    for i in range(size):
                        board[row + i][col] = 'O'
                        ship_positions[ship].append((row + i, col))
                    placed = True
    return ship_positions


def computer_guess(board, last_hit=None):
    """
    Computer guesses. If last_hit is provided, guesses adjacent cells first.
    """
    if last_hit:
        row, col = last_hit
        # Directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # Randomize directions to add unpredictability
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 9 and 0 <= new_col < 9 and board[new_row][new_col] == ' ':
                return new_row, new_col

    # If no last hit or no valid adjacent spots, choose a random empty cell
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
