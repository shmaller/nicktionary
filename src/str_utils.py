'''String manipulation utilities and longer strings.'''

import time
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

IN_GAME_INSTRUCTIONS = dedent(
    """
    Type 'help' to read the rules of the game.
    Type 'quit' at any time to end the game.
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

def print_wordle_date_header(wordle_date):
    '''Prints to the console which date has been chosen for the Wordle solution.

    Input: wordle_date (str): Date corresponding to Wordle solution.

    Returns: None.
    '''
    print(dedent(
        f"""
        Playing Wordle from {wordle_date}.
        ---------------------------------------------------------------------------"""
        )
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

def pad_str(str):
    '''Pads str with internal spaces.

    Input: str (str): In string.

    Returns: str with spaces between each character.
    '''
    outstr = ''
    for char in str:
        outstr += char + ' '

    return outstr.strip()

def crawl(str):
    '''Crawls str across the screen slowly.

    Input: str (str): String to crawl.

    Returns None.
    '''
    for char in str:
        time.sleep(0.1)
        print(char,end='',flush=True)

def splice_str(str,letter,index):
    '''Inserts letter into str at index.

    Inputs:
    - str (str): String to insert letter into.
    - letter (str): Letter to insert into str.
    - index (int): Index in str at which to insert letter.

    Returns: Spliced string (str)
    '''
    new_header = str[0:index] + letter
    new_footer = ''

    if str[index:]:
        new_footer = str[index+1:]

    return new_header + new_footer