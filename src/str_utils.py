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
    stats: See your playing statistics.
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

def generate_wordle_date_header(wordle_date):
    '''Prints to the console which date has been chosen for the Wordle solution.

    Input: wordle_date (str): Date corresponding to Wordle solution.

    Returns: None.
    '''
    print(dedent(
        f"""
        Playing Wordle from {wordle_date}.
        ---------------------------------------------------------------------------"""
    )

def gen_stats_breakdown_str(play_count, stats_breakdown):
    return dedent(
        f'''\

        You've played {play_count} times.

        Here's how many guesses it's taken you to get the answer:

        1: {stats_breakdown[1]}
        2: {stats_breakdown[2]}
        3: {stats_breakdown[3]}
        4: {stats_breakdown[4]}
        5: {stats_breakdown[5]}
        6: {stats_breakdown[6]}

        Won: {stats_breakdown['won']}
        Lost: {stats_breakdown['lost']}

        (ENTER to continue)
        '''
    )

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