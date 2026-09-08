'''Longer strings and input testing functionality.'''

from textwrap import dedent

SPLASH = dedent(
    """
    N I C K T I O N A R Y
    ---------------------------------------------------------------------------

    Welcome to Nicktionary! Try to guess the word!
    This program replicates Josh Wardle\'s game Wordle.
    It loads a new wordle every day, and is playable until October 20, 2027.
    Run this program every day to play a new word!
    """
)

MAIN_MENU = dedent(
    """
        *************
        * MAIN MENU *
        *************

    Type a command and hit ENTER:

    play: Play today's word.
    random: Play a word from a random date.
    date: Play a word from a specific date.
    help: Read the rules of the game.
    quit: Exit the program.

    """
)

WORDLE_LIST_NOT_FOUND = dedent(
    """
    *****************************************************************
    ERROR: Cannot find solution list. 

    Make sure 'wordle_list.txt' exists in the same directory 
        as this program. 

    Press ENTER to quit, place the file in this directory,
        and then try again.
    *****************************************************************
    """
)

def prompt(prompt, options=[]):
    '''Prompt the user for input, optionally check against valid values.

    Inputs:
    - prompt (str): Prompt to show to user.
    - options (list[str]) (optional): List of valid options.

    Raises: ValueError if options AND user response not in options.

    Returns: User response to prompt, stripped, uppercase (str).
    '''
    response = input(prompt).strip().upper()

    if options and response not in options:
        raise ValueError(f"Response '{response}' not in options {options}.")

    return response