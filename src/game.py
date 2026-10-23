import sys
import time

import str_utils
import exceptions
import dictionary
import evaluate
# from game_stat import Stat

class Game:
    def __init__(self, date, wordle):
        self.date = date
        self.wordle = wordle
        # self.stat = Stat(date)
        self.won = False

    def play(self):
        '''Evaluates user guesses against solution word, prints progress to console.

        Input: wordle (str): Solution word

        Returns: None.
        '''
        print(str_utils.generate_wordle_date_header(self.date))
        print(str_utils.IN_GAME_INSTRUCTIONS)

        won = False
        i = 1 # 1-index makes for prettier display
        while i < 7:
            guess = input(f'GUESS #{i}: ').upper().strip()

            if guess == 'QUIT':
                sys.exit(0)
            elif guess == 'HELP':
                help.help()
                continue

            try:
                _is_valid(guess)
            except exceptions.GuessWrongLength:
                print('Guess must be a five-letter word!')
                continue
            except (exceptions.GuessNotAlphaNumeric, exceptions.NumberInGuess):
                print('Letters only!')
                continue
            except exceptions.GuessnNotInDictionary:
                print("That word's not in the dictionary!")
                continue

            evaluation = evaluate.evaluate_guess(guess,self.wordle)
            # self.stat.add_guess(i,evaluation)

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
        raise exceptions.GuessWrongLength()
    if not guess.isalnum():
        raise exceptions.GuessNotAlphaNumeric()
    for i in range(10):
        if str(i) in guess:
            raise exceptions.NumberInGuess()
    if not dictionary.in_dictionary(guess):
        raise exceptions.GuessnNotInDictionary()
