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
import str_utils
import fileops

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
        guess = str_utils.prompt(f'GUESS #{i+1}: ')

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
    fileops.check_for_wordle_file()
    
    print(str_utils.SPLASH)
    time.sleep(1.5)

    while True:
        try:
            response = str_utils.prompt(
                str_utils.MAIN_MENU,
                ['PLAY','RANDOM','DATE','HELP','QUIT']
            )
        except ValueError:
            print('\nInvalid input.')
            time.sleep(1)
            continue

        if response == 'PLAY':
            play(fileops.read_wordle('TODAY'))

        elif response == 'RANDOM':
            play(fileops.read_wordle('RANDOM'))
        
        elif response == 'DATE':
            str_date = str_utils.prompt("Enter a date in the format YYYYMMDD: ")
            try:
                play(fileops.read_wordle('DATE',str_date))
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