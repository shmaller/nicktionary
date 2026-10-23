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

import help
import str_utils
import fileops
from game import Game
from stats_manager import StatsManager

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

def main():
    '''Main loop: Prompts user input for game mode, then plays game.

    Inputs: None.

    Returns: None.
    '''
    fileops.check_for_wordle_file()
    stats_manager = StatsManager()
    
    print(str_utils.SPLASH)
    time.sleep(1.5)

    while True:
        response = input(str_utils.MAIN_MENU).upper().strip()

        if response == 'PLAY':
            date = fileops.determine_wordle_date('TODAY')
        elif response == 'RANDOM':
            date = fileops.determine_wordle_date('RANDOM')
        elif response == 'DATE':
            str_date = input("Enter a date in the format YYYYMMDD: ")
            try:
                date = fileops.determine_wordle_date('DATE',str_date)
            except ValueError:
                print(
                    '\nTry again! Date must be between June 19, 2021\n'
                    '   and October 20, 2027, and in format YYYYMMDD.\n'
                )
                time.sleep(1)
                continue
        elif response == 'HELP':
            help.help()
            continue
        elif response == 'STATS':
            stats_manager.display()
            continue
        elif response == 'QUIT':
            sys.exit(0)
        else:
            print('\nInvalid input.')
            time.sleep(1)
            continue

        wordle = fileops.read_wordle(date)
        game = Game(date, wordle)
        game.play()

        stats_manager.add_stat(game.stat)
        stats_manager.save()

if __name__ == '__main__':
    config_logging()
    main()
