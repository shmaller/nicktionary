'''Nicktionary
Nicholas Boni
December 12, 2023
'''
import os
import sys
import time
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

import evaluate
import help
import str_utils
import fileops
import dictionary

def config_logging():
    '''Configure logging for main application.'''
    formatter = Formatter(
        '{asctime} [{levelname}] {filename} {funcName}({lineno}): {message}', 
        style = '{'
    )

    os.makedirs('log', exist_ok = True)
    file_handler = RotatingFileHandler(
        filename = 'log/nicktionary.log',
        maxBytes = 102400,
        backupCount = 3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.addHandler(file_handler)

def play(wordle):
    '''Evaluates user guesses against solution word, prints progress to console.

    Input: wordle (str): Solution word

    Returns: None.
    '''
    print(str_utils.IN_GAME_INSTRUCTIONS)

    i = 0
    won = False
    while i < 6:
        guess = input(f'GUESS #{i+1}: ').upper().strip()

        if guess == 'QUIT':
            sys.exit(0)
        elif guess == 'HELP':
            help.help()
            continue            
        if not _is_valid(guess):        
            print('Invalid guess!')
            continue

        evaluation = evaluate.evaluate_guess(guess,wordle)
        print(str_utils.pad_str(guess))
        str_utils.crawl(evaluation + '\n\n')

        if evaluation == 'O O O O O':
            won = True
            break

        i += 1
    
    if won:
        time.sleep(0.5)
        str_utils.crawl('!!! W I N N E R !!!')
        time.sleep(1)
        print('\n\nYou won!')
    else:
        time.sleep(1)
        print('Oh no!...')
        time.sleep(2)
        print(f'\nYou lost. The word was {wordle}.')
    
    time.sleep(3)
    print('\nRun me tomorrow to play again!')
    time.sleep(2)
    input('\nPress ENTER to return to the main menu.')
    print('\nSee you tomorrow!')
    time.sleep(1)
    str_utils.crawl('love, N\n')
    time.sleep(1.25)
    
def _is_valid(guess):
    '''Tests if guess meets basic validity check.

    Input: guess (str): User guess to check.

    Returns:
    - True if guess is valid.
    - False otherwise.
    '''
    if len(guess) != 5:
        return False
    if not guess.isalnum():
        return False
    for i in range(10):
        if str(i) in guess:
            return False
    if not dictionary.in_dictionary(guess):
        return False
    
    return True

def main():
    '''Main loop: Prompts user input for game mode, then plays game.

    Inputs: None.

    Returns: None.
    '''
    fileops.check_for_wordle_file()
    
    print(str_utils.SPLASH)
    time.sleep(1.5)

    while True:
        response = input(str_utils.MAIN_MENU).upper().strip()

        if response == 'PLAY':
            play(fileops.read_wordle('TODAY'))
        elif response == 'RANDOM':
            play(fileops.read_wordle('RANDOM'))
        elif response == 'DATE':
            str_date = input("Enter a date in the format YYYYMMDD: ")
            try:
                play(fileops.read_wordle('DATE',str_date))
            except ValueError:
                print(
                    '\nTry again! Date must be between June 19, 2021\n'
                    '   and October 20, 2027, and in format YYYYMMDD.\n'
                )
                time.sleep(1)
        elif response == 'HELP':
            help.help()
        elif response == 'QUIT':
            sys.exit(0)
        else:
            print('\nInvalid input.')
            time.sleep(1)

if __name__ == '__main__':
    config_logging()
    main()