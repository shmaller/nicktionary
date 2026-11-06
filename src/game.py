import sys
import time

import str_utils
import exceptions
import dictionary
import evaluate
import help
from game_stat import Stat
from valid_letters import ValidLetters
from hard_mode_sequence import HardModeSequence

class Game:
    '''Represents a single Nicktionary playthrough. 
        Tracks stats in a game_stat.Stat object.

    Inputs:
    - date (str): Date of desired solution word 
        (from fileops.determine_wordle_date)
    - wordle (str): Solution word.
    - difficulty (str): Game difficulty ('NORMAL' or 'HARD').
    '''
    def __init__(self, date, wordle, difficulty):
        self.date = date
        self.wordle = wordle
        self.difficulty = difficulty
        self.stat = Stat(date)
        self.won = False
        self.complete = False

    def play(self):
        '''Evaluates user guesses against solution word, prints progress to console.

        Inputs: None.

        Returns: None.
        '''
        print(str_utils.generate_wordle_date_header(self.date, self.difficulty))
        print(str_utils.IN_GAME_INSTRUCTIONS)

        won = False
        valid_letters = ValidLetters()
        if self.difficulty == 'HARD':
            hard_mode_sequence = HardModeSequence()
        else:
            hard_mode_sequence = None
        
        i = 1
        while i < 7:
            guess = input(f'GUESS #{i}: ').upper().strip()

            if guess == 'QUIT':
                sys.exit(0)
            elif guess == 'BACK':
                return
            elif guess == 'HELP':
                help.help()
                continue
            elif guess == 'LETTERS':
                print(f'Remaining letters:\n{valid_letters.letters}')
                print(f'Eliminated letters:\n{valid_letters.eliminated}')
                continue

            try:
                _is_valid(guess, hard_mode_sequence)
            except exceptions.GuessWrongLength:
                print('Guess must be a five-letter word!')
                continue
            except (exceptions.GuessNotAlphaNumeric, exceptions.NumberInGuess):
                print('Letters only!')
                continue
            except exceptions.GuessNotInDictionary:
                print("That word's not in the dictionary!")
                continue
            except exceptions.HardModeRule:
                print('HARD MODE: Your guess must make use of all the information\n'
                "you've been given by previous evaluations. "
                "Type 'help' for details.\n"
                "See the Game Difficulty section.")
                continue

            evaluation = evaluate.evaluate_guess(
                guess, self.wordle, valid_letters, hard_mode_sequence
            )

                
            self.stat.add_guess(i,evaluation)

            print(str_utils.pad_str(guess))
            str_utils.crawl(evaluation + '\n\n')

            if evaluation == 'O O O O O':
                won = True
                break

            i += 1

        self.complete = True
        if won:
            time.sleep(0.5)
            str_utils.crawl('!!! W I N N E R !!!')
            time.sleep(1)
            print('\n\nYou won!')
        else:
            time.sleep(1)
            print('Oh no!...')
            time.sleep(2)
            print(f'\nYou lost. The word was {self.wordle}.')
        
        time.sleep(3)
        print(f"\nHere's your results code:\n\n{self.stat.share_code()}")
        input('\nPress ENTER to return to the main menu.')
        print('\nRun me tomorrow to play again!')
        time.sleep(2)
        print('\nSee you tomorrow!')
        time.sleep(1)
        str_utils.crawl('love, N\n')
        time.sleep(1.25)
    
def _is_valid(guess, hard_mode_sequence):
    '''Tests if guess meets basic validity check.

    Inputs: 
    - guess (str): User guess to check.
    - hard_mode_sequence (hard_mode_sequence.HardModeSequence): Sequence 
        to check against (self.difficulty == 'HARD' only).
        If self.difficulty == 'NORMAL', pass None here.

    Raises:
    - exceptions.GuessWrongLength() if len(guess) != 5
    - exceptions.GuessNotAlphaNumeric() if not guess.isalnum()
    - exceptions.NumberInGuess() if a number is in the guess
    - exceptions.GuessNotInDictionary() guess not in dictionary
    - exceptions.HardModeRule if hard_mode_sequence is not None 
        AND fails sequence.validate_guess()

    Returns: None.
    '''
    if len(guess) != 5:
        raise exceptions.GuessWrongLength()
    if not guess.isalnum():
        raise exceptions.GuessNotAlphaNumeric()
    for i in range(10):
        if str(i) in guess:
            raise exceptions.NumberInGuess()
    if not dictionary.in_dictionary(guess):
        raise exceptions.GuessNotInDictionary()
    if hard_mode_sequence is not None:
        hard_mode_sequence.validate_guess(guess)
