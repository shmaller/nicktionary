import str_utils

'''Methods to interact with the solution file.'''

def check_for_wordle_file():
    '''Aborts execution if solution list not found in this directory.'''
    if not os.path.isfile(_resource_path('wordle_list.txt')):
        logger.critical('wordle_list.txt not found in this directory. Aborting.')
        input(str_utils.WORDLE_LIST_NOT_FOUND)
        sys.exit(1)

def read_wordle(option, indate=''):
    '''Reads solution word from given game mode from solution file.

    Inputs:
    - option (str): One of 'today', 'random', 'date'.
    - indate (str) (required for 'date'): Specific date to play.

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
    
    with open(_resource_path('wordle_list.txt')) as f:
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

def _resource_path(relative_path):
    '''Get absolute path to resource, works for dev and for PyInstaller.
    (copied from StackOverflow:
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
    
    '''
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)