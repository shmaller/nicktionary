'''Nicktionary
Nicholas Boni
December 12, 2023
'''
import os
import sys
import time
import datetime
import random
import logging
import textwrap
from logging import Formatter
from logging.handlers import RotatingFileHandler

import evaluate
import help
import interface
import str_utils

logger = logging.getLogger(__name__)

def config_logging():
    '''Configure logging for main application.'''
    formatter = Formatter(
        '{asctime} [{levelname}] {filename} {funcName}({lineno}): {message}', 
        style = '{'
    )

    os.makedirs('log', exist_ok = True)
    file_handler = RotatingFileHandler(
        filename = 'log/nicktionary.log',
        maxBytes = 1024,
        backupCount = 3
    )
    
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def resource_path(relative_path):
    '''Get absolute path to resource, works for dev and for PyInstaller.
    (copied from StackOverflow:
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
    
    '''
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def check_for_wordle_file():
    '''Aborts execution if solution list not found in this directory.'''
    if not os.path.isfile(resource_path('wordle_list.txt')):
        logger.critical('wordle_list.txt not found in this directory. Aborting.')
        input(interface.WORDLE_LIST_NOT_FOUND)
        sys.exit(1)

def read_wordle(option, indate=''):
    '''Reads solution word from given game mode from solution file.

    Inputs:
    option (str): One of 'today', 'random', 'date'.
    indate (str) (required for 'date'): Specific date to play.

    Raises: ValueError if option not in ['today', 'random', 'date'].

    Returns: Solution word (str)
    '''
    if option == 'TODAY':
        wordle_date = datetime.date.today().strftime('%b %d %Y')
    
    elif option == 'RANDOM':
        start_date = datetime.date(2021, 6, 19) # first date in wordle_list
        rand_days = random.choice(range(2314)) # number of unique dates in wordle_list
        random_date = start_date + datetime.timedelta(days=rand_days)

        wordle_date = random_date.strftime('%b %d %Y')

    elif option == 'DATE':
        year = int(indate[0:4])
        month = int(indate[4:6])
        day = int(indate[6:8])

        wordle_date = datetime.date(year, month, day).strftime('%b %d %Y')

    else:
        raise ValueError(
            f"Invalid option {option}, must be one of "
            "'today','random', 'date'."
        )

    wordle = ''
    
    with open(resource_path('wordle_list.txt')) as f:
        for line in f:
            line_list = line.split()
            filedate = str_utils.pad_str(line_list[0:3])
            if filedate == wordle_date:
                wordle = line_list[-1]
                break

    if not wordle:
        print("\nToday's date not found. Choosing a random date.")
        return read_wordle('random')

    print(textwrap.dedent(
        f"""
        Playing Wordle from {wordle_date}.
        ---------------------------------------------------------------------------"""
        )
    )

    return wordle

def play(wordle):
    '''Evaluates user guesses against solution word, prints progress to console.

    Inputs:
    - wordle (str): Solution word

    Returns: None.
    '''
    print(textwrap.dedent(
        """
        Type 'help' to read the rules of the game.
        Type 'quit' at any time to end the game.
        """
        )
    )

    i = 0
    won = False
    while i < 6:
        guess = interface.prompt(f'GUESS #{i+1}: ')

        if guess == 'QUIT':
            sys.exit(0)
        elif guess == 'HELP':
            help.help()
            continue

        if len(guess) != 5 or not guess.isalnum():
            print('Invalid guess!')
            continue

        print(str_utils.pad_str(guess.upper()))
        outstr = str_utils.pad_str(evaluate.evaluate_guess(guess,wordle))
        print(outstr + '\n')

        if outstr == 'O O O O O':
            won = True
            break

        i += 1
    
    if won:
        time.sleep(0.5)
        crawl('!!! W I N N E R !!!')
        time.sleep(1)
        print('\n\nYou won!')
    else:
        time.sleep(1)
        print('Oh no!...')
        time.sleep(2)
        print(f'\nYou lost. The word was {wordle}.')
    
    time.sleep(3)
    print('\nRun me tomorrow to play again!')
    time.sleep(3)
    input('\nPress ENTER to quit.')
    print('\nSee you tomorrow!')
    time.sleep(1)
    crawl('love, N')
    time.sleep(1.25)
    
    sys.exit(0)

def main():
    '''Main loop: Prompts user input for game mode, then plays game.

    Inputs: None.

    Returns: None.
    '''
    check_for_wordle_file()
    
    print(interface.SPLASH)
    time.sleep(1.5)

    while True:
        try:
            response = interface.prompt(
                interface.MAIN_MENU,
                ['PLAY','RANDOM','DATE','HELP','QUIT']
            )
        except ValueError:
            print('\nInvalid input.')
            time.sleep(1)
            continue

        if response == 'PLAY':
            play(read_wordle('TODAY'))

        elif response == 'RANDOM':
            play(read_wordle('RANDOM'))
        
        elif response == 'DATE':
            str_date = interface.prompt("Enter a date in the format YYYYMMDD: ")
            try:
                play(read_wordle('DATE',str_date))
            except ValueError:
                print('\nInvalid date. Try again!\n')
                time.sleep(1)
                continue
        
        elif response == 'HELP':
            help.help()
        
        elif response == 'QUIT':
            sys.exit(0)

if __name__ == '__main__':
    config_logging()
    main()