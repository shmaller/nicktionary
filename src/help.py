'''Plays the tutorial.'''

import sys
import time
from textwrap import dedent

import str_utils

def help():
    '''Plays the interactive tutorial.

    Inputs: None.

    Returns: None.
    '''
    input(
        dedent(
            """\
            ------------------------------------------------------
            HOW TO PLAY              

            Your objective is to guess the five-letter word.
            
            When you submit your guess, the program will tell you
            whether each letter of your guess appears in the 
            solution word.

            ------------------------------------------------------
            (ENTER to continue)"""
        )
    )

    _delete_last_line()

    print("Here's an example:\n")
    time.sleep(1.5)

    str_utils.crawl('paste')
    time.sleep(1)
    print('\n\nP A S T E')
    print('O O X O -')
    time.sleep(2)

    input(
        dedent(
            """
            This means that the letters P, A, and T are correct.
            The answer will look like: PA_T_.

            The letter S appears somewhere in the solution, 
            but not as the third letter.

            The letter E does not appear in the solution word.

            (ENTER to continue)"""
        )
    )

    _delete_last_line()

    print("A good second guess might be PARTS. Let's try it:\n")
    time.sleep(1.5)

    str_utils.crawl('parts')
    time.sleep(1)
    print('\n\nP A R T S')
    print('O O - O O')
    time.sleep(2)

    input(
        dedent(
        """
        Hmm... So the solution is PA_TS. How about PANTS?

        (ENTER to continue)"""
        )
    )

    _delete_last_line()

    str_utils.crawl('pants')
    time.sleep(1)
    print('\n\nP A N T S')
    print('O O O O O')
    time.sleep(2)

    input(
        dedent(
            """
            Whew, we got it!
                        
            (ENTER to finish)"""
        )
    )
    _delete_last_line()
    
    print("You have six guesses to get it right!")
    time.sleep(2)
    print("\nNow you're ready to play!\n")
    time.sleep(2)

def _delete_last_line():
    '''Erases previous line in terminal and sets starting point there.
    Removes (ENTER to continue) lines and starts again from there.

    Inputs: None.

    Returns: None.
    '''
    sys.stdout.write('\x1b[1A') # cursor up one line
    sys.stdout.write('\x1b[2K') # delete last line
