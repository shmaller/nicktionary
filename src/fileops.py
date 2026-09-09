'''Methods to interact with the solution file.'''

import os
import sys
import datetime
import textwrap
import random
import logging

import str_utils

NUMBER_OF_WORDLES = 2315
START_DATE = datetime.date(2021, 6, 19) # first date in wordle_list

logger = logging.getLogger(__name__)

def check_for_wordle_file():
    '''Aborts execution if solution list not found in this directory.'''
    if not os.path.isfile(_resource_path('wordle_list.txt')):
        logger.critical('wordle_list.txt not found in this directory. Aborting.')
        input(str_utils.WORDLE_LIST_NOT_FOUND)
        sys.exit(1)

def _resource_path(relative_path):
    '''Get absolute path to resource, works for dev and for PyInstaller.
    (copied from StackOverflow:
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
    '''
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def read_wordle(option, indate=''):
    '''Reads solution word from given game mode from solution file.

    Inputs:
    - option (str): One of 'today', 'random', 'date'.
    - indate (str) (required for 'date'): Specific date to play.

    Returns: Solution word (str)
    '''
    wordle_date = _determine_wordle_date(option, indate)
    wordle = ''
    
    with open(_resource_path('wordle_list.txt')) as f:
        for line in f:
            line_list = line.split()
            filedate = str_utils.pad_str(line_list[0:3])
            if filedate == wordle_date:
                wordle = line_list[-1]
                break

    if not wordle:
        print("\nToday's date not found. Choosing a random date.")
        return read_wordle('RANDOM')

    str_utils.print_wordle_date_header(wordle_date)

    return wordle

def _determine_wordle_date(option, indate):
    '''
    Inputs:
    - option (str): User-requested game mode.
    - indate (str): Requested date. Used for 'DATE' mode. Must be 8 chars.

    Raises: 
    - ValueError if indate not in valid date range.
    - ValueError if indate not 8 chars long.
    - ValueError if option not in ['TODAY','RANDOM','DATE'].

    Returns: (str) Requested date, to be used to choose proper solution word.
    '''
    if option == 'TODAY':
        return datetime.date.today().strftime('%b %d %Y')
    
    elif option == 'RANDOM':
        rand_days = random.choice(range(NUMBER_OF_WORDLES))
        random_date = START_DATE + datetime.timedelta(days=rand_days)

        return random_date.strftime('%b %d %Y')

    elif option == 'DATE':
        if not len(indate) == 8:
            raise ValueError(f"Indate was not 8 characters: {indate}")

        str_year = indate[0:4]
        str_month = _strip_leading_zero(indate[4:6])
        str_day = _strip_leading_zero(indate[6:8])
        
        year = int(str_year)
        month = int(str_month)
        day = int(str_day)

        selected_date = datetime.date(year, month, day)
        valid_range = _generate_date_range()
        
        if selected_date not in valid_range:
            raise ValueError(f'User-provided date {selected_date} not in valid date range.')

        return selected_date.strftime('%b %d %Y')

    else:
        raise ValueError(
            f"Invalid option {option}, must be one of "
            "'today','random', 'date'."
        )

def _generate_date_range():
    '''Generates list of dates with Wordle solutions.
    For comparison with user-selected date.

    Inputs: None.

    Returns: List of 2315 datetime.dates corresponding to Wordle solutions.
    '''
    return [START_DATE + datetime.timedelta(i) for i in range(NUMBER_OF_WORDLES)]

def _strip_leading_zero(two_digit_number):
    '''Months and days sometimes have leading zeroes which are syntactically
    incorrect with datetime. Strip them out.
    
    Input: two_digit_number (str): Month or day, possibly with leading zero (e.g., 04)

    Returns: Just the significant digit(s). If no leading zero, untouched.    
    '''
    return two_digit_number[-1] if two_digit_number[0] == '0' else two_digit_number