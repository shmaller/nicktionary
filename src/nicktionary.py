'''
Nicktionary
Nicholas Boni
December 12, 2023
'''
import os
import sys
import time
import datetime
import random
import logging

def config_logging()
    logger = logging.getLogger(__name__)

    formatter = logger.Formatter(
        '{asctime} [{levelname}] {filename} {funcName}({lineno}): {message}', 
        style = '{'
    )
    stream_handler = logging.StreamHandler()
    file_handler = logging.RotatingFileHandler(
        filename = 'log/nicktionary.log',
        maxBytes = 1024,
        backupCount = 3
    )

    logger.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

def resource_path(relative_path):
    '''
    Get absolute path to resource, works for dev and for PyInstaller.
    (copied from StackOverflow:
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
    '''
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def evaluate_guess(guess,answer):
    '''
    Accepts guess, answer as str.

    Checks each letter of guess against all letters in answer.
    Constructs outstr containing '-','X','O' if guess letter is
    missing, in wrong place, or correct.

    Returns outstr.
    '''
    outstr = '.....'
    guess_i = 0
    start_over = False
    while guess_i < len(guess):
        action_taken = False
        guess_letter = guess[guess_i]

        # skip results already rendered
        if guess_letter == '_':
            guess_i += 1
            continue # continue guess loop

        answer_i = 0
        while answer_i < len(answer) and not start_over:
            answer_letter = answer[answer_i]

            # does this letter appear in the solution?
            if guess_letter == answer_letter:
                    # letter appears in solution.

                    # is it in the correct place?
                    if guess_i == answer_i: 
                        outstr = splice_str(outstr,'O',guess_i)
                        guess = splice_str(guess,'_',guess_i)
                        answer = splice_str(answer,'_',guess_i)
                        action_taken = True
                        break # break answer loop.

                    # !(guess_letter == answer_letter)
                    # letter in solution, but not at this index
                    else: 
                        # is this letter repeated in guess? if so,
                        # check future instance for correctness
                        if guess_letter in guess[guess_i+1:]:
                            guess_j = guess_i+1

                            while guess_j < len(guess):
                                if guess[guess_j] == answer[guess_j]:

                                    # '_' matches are meaningless
                                    if guess[guess_j] == '_':
                                        break # break future letter loop
                                    
                                    outstr = splice_str(outstr,'O',guess_j)
                                    guess = splice_str(guess,'_',guess_j)
                                    answer = splice_str(answer,'_',guess_j)
                                    action_taken = True
                                    start_over = True
                                    break # break future letter loop

                                guess_j += 1

                        # !(guess_letter in guess[guess_i+1:])
                        # guess letter not repeated in guess
                        else:
                            # does this letter appear in the answer
                            # in the future?
                            if guess_letter in answer[answer_i+1:]:
                                answer_i += 1
                                continue # continue answer loop

                            # !(guess_letter in answer[answer[i+1:]])
                            # this letter does not appear in the answer
                            # in the future.
                            else:
                                outstr = splice_str(outstr,'X',guess_i)
                                guess = splice_str(guess,'_',guess_i)
                                answer = splice_str(answer,'_',answer_i)
                                action_taken = True
                                start_over = True
                                break # break answer loop
    
            if start_over:
                break # break answer loop
            
            # END ANSWER LOOP
            answer_i += 1 

        if start_over:
            start_over = False
            guess_i = 0
            continue # continue guess loop
        
        # this letter does not appear in the solution
        if not action_taken:
            outstr = splice_str(outstr,'-',guess_i)
        
        # END GUESS LOOP
        guess_i += 1

    return(outstr)

def splice_str(str,letter,index):
    '''
    Accepts an input str, the letter to splice into the input str,
    and the index at which to splice it as inputs.

    Replaces char in str with letter.

    Returns updated str.
    '''
    new_header = str[0:index] + letter
    new_footer = ''

    if str[index:]:
        new_footer = str[index+1:]

    return new_header + new_footer

def pad_str(str):
    '''
    Accepts str as input.

    Pads str with spaces between all elements internally.
    Spaces are removed from ends.

    Returns outstr. 
    '''
    outstr = ''
    for char in str:
        outstr += char + ' '

    return outstr.strip()

def read_wordle(option, indate=''):
    '''
    Accepts infile with list of all wordle solutions.

    Grabs today's date, scans infile for appropriate 
    wordle solution.

    Returns wordle solution as str.
    '''

    if option == 'today':
        wordle_date = datetime.date.today().strftime('%b %d %Y')
    
    elif option == 'random':
        start_date = datetime.date(2021, 6, 19) # first date in wordle_list
        rand_days = random.choice(range(2314)) # number of unique dates in wordle_list

        random_date = start_date + datetime.timedelta(days=rand_days)
        wordle_date = random_date.strftime('%b %d %Y')

    elif option == 'date':
        try:
            year = int(indate[0:4])
            month = int(indate[4:6])
            day = int(indate[6:8])

            wordle_date = datetime.date(year, month, day).strftime('%b %d %Y')
        except ValueError:
            logger.error(f'Invalid year, month, or day: {year} {month} {day}; '
                        'can\'t cast as int.')
            raise

    else:
        raise ValueError(
            "Invalid option {option}, must be one of "
            "'today','random', 'date'."
        )

    wordle = ''

    if not os.path.isfile(resource_path('wordle_list.txt')):
        print("""
*****************************************************************
ERROR: Cannot find solution list. 
Make sure 'wordle_list.txt' exists in the same 
directory as this program. 
Press ENTER to quit, place the file in this directory,
and then try again.
*****************************************************************
""")
        input()
        sys.exit()
    
    with open(resource_path('wordle_list.txt')) as f:
        for line in f:
            line_list = line.split()
            filedate = pad_str(line_list[0:3])
            if filedate == wordle_date:
                wordle = line_list[-1]
                break

    if not wordle:
        print('\nToday\'s date not found. Choosing a random date.')
        return read_wordle('random')

    print(f"""
Playing Wordle from {wordle_date}.
---------------------------------------------------------------------------""")
    return wordle

def delete_last_line():
        #cursor up one line
        sys.stdout.write('\x1b[1A')
        #delete last line
        sys.stdout.write('\x1b[2K')

def crawl(str):
    '''
    Accepts str as input.

    Crawls str across the screen slowly.

    Returns None.
    '''
    for char in str:
        time.sleep(0.1)
        print(char,end='',flush=True)

def help():
    input("""
------------------------------------------------------
HOW TO PLAY              

Your objective is to guess the five-letter word.
When you submit your guess, the program will tell you
    whether each letter of your guess appears in the 
    solution word.

------------------------------------------------------
(ENTER to continue)""")

    delete_last_line()

    print("Here's an example:\n")
    time.sleep(1.5)

    crawl('paste')
    time.sleep(1)
    print('\n\nP A S T E')
    print('O O X O -')
    time.sleep(2)

    input("""
This means that the letters P, A, and T are correct.
The answer will look like: PA_T_.

The letter S appears somewhere in the solution, 
            but not as the third letter.

The letter E does not appear in the solution word.

(ENTER to continue)""")

    delete_last_line()

    print("A good second guess might be PARTS. Let's try it:\n")
    time.sleep(1.5)

    crawl('parts')
    time.sleep(1)
    print('\n\nP A R T S')
    print('O O - O O')
    time.sleep(2)

    input("""
Hmm... So the solution is PA_TS. How about PANTS?

(ENTER to continue)""")

    delete_last_line()

    crawl('pants')
    time.sleep(1)
    print('\n\nP A N T S')
    print('O O O O O')
    time.sleep(2)

    input("""
Whew, we got it!
            
(ENTER to finish)""")
            
    delete_last_line()
    
    print("You have six guesses to get it right!")
    time.sleep(2)
    print("\nNow you're ready to play!\n")
    time.sleep(2)

def play(wordle):
    print("""
Type 'help' to read the rules of the game.
Type 'quit' at any time to end the game.
""")

    i = 0
    won = False
    while i < 6:
        guess = input(f'GUESS #{i+1}: ').strip().upper()

        if guess == 'QUIT':
            sys.exit()

        elif guess == 'HELP':
            help()
            continue

        if len(guess) != 5 or not guess.isalnum():
            print('Invalid guess!')
            continue

        print(pad_str(guess))
        outstr = evaluate_guess(guess,wordle)
        outstr = pad_str(outstr)
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
    
    sys.exit()

def main():
    '''
    '''

    print("""
N I C K T I O N A R Y
---------------------------------------------------------------------------

Welcome to Nicktionary! Try to guess the word!
This program replicates Josh Wardle\'s game Wordle.
It loads a new wordle every day, and is playable until October 20, 2027.
Run this program every day to play a new word!
""")
    time.sleep(1.5)

    while True:
        response = input("""
    *************
    * MAIN MENU *
    *************\n
Type a command and hit ENTER:\n
play: Play today's word.
random: Play a word from a random date.
date: Play a word from a specific date.
help: Read the rules of the game.
quit: Exit the program.\n\n""")

        if response.lower() == 'play':
            play(read_wordle('today'))

        elif response.lower() == 'random':
            play(read_wordle('random'))
            
        elif response.lower() == 'date':
            str_date = input("Enter a date in the format YYYYMMDD: ")
            try:
                play(read_wordle('date',str_date))
            except ValueError:
                print('\nInvalid date. Try again!\n')
                time.sleep(1.5)
            
        elif response.lower() == 'help':
            help()

        elif response.lower() == 'quit':
            sys.exit(0)
        
        else:
            print('\nInvalid input.')
            time.sleep(1.5)

if __name__ == '__main__':
    main()