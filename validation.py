import time
import gspread
from google.oauth2.service_account import Credentials
from email_validator import validate_email, EmailNotValidError
from colors import Color as Col
from run import run_game, cls, separate_line


# Scope and constant vars defined as in love_sandwiches walk-through project
# by Code Institute
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


def log_in_player():
    """
    Logs in a single player using their email address.
    Retrieves the player's name from the first row and their score from the third column of the spreadsheet.
    """
    print(Col.GREEN + "Welcome back! Please help me verify your login details.")

    try:
        while True:
            email = get_email("Player")
            existing_player = is_player_registered(email)

            if existing_player:
                # Get the player's row and details
                player_row = WORKSHEET.find(email).row
                player_name = WORKSHEET.row_values(player_row)[0]
                player_score = int(WORKSHEET.row_values(player_row)[2])

                print(Col.BLUE + f"\nHello {player_name}!\n")
                print(Col.YELLOW + f"Your current score is: {player_score}\n")

                time.sleep(2)
                start_game_message(player_name)
                return {"name": player_name, "email_row": player_row, "score": player_score}
            else:
                input_correct_email("Player")

    except Exception as e:
        print(Col.RED + f"An error occurred: {e}")
        return None


def get_email(playername: str) -> str:
    """
    Ask user to input their email address
    @param playername(string): Player's number
    """
    while True:
        email = input(f"{playername} - what's your email address?\n").strip()

        if validate_user_email(email):
            break

    return email        