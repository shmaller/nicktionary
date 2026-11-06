import str_utils
import exceptions

class HardModeSequence:
    '''Sequence of letters a user must abide by once they have discovered
    them while playing in HARD mode.
    '''
    def __init__(self):
        self.sequence = '-----'
        self.x_letters = []

    def update_sequence(self, guess, eval_str):
        '''Once a guess has been evaluated, update the sequence we have
        on record to compare against in future guesses.

        Inputs:
        - guess (str): User's guess.
        - eval_str (str): Evaluation of user's guess by evaluate.evaluate_guess()
            (BEFORE padding the outstr, e.g., OX-XO).
        
        Returns: None.
        '''
        i = 0
        while i < 5:
            if eval_str[i] == 'O':
                self.sequence = str_utils.splice_str(
                    self.sequence, guess[i], i
                )
            i += 1

        i = 0
        while i < 5:
            if eval_str[i] == 'X':
                self.x_letters.append(guess[i])
            i += 1

    def validate_guess(self, guess):
        '''Given a guess, test against self.sequence and self.x_letters
        to determine if the guess is valid along HARD mode rules.

        Input: guess (str): User's guess

        Raises exceptions.HardModeRule if:
        - Non-'-' characters in self.sequence do not match characters in guess
            at same index (guess doesn't contain all O matches).
        - After removing all 'X' letters found in the guess from self.x_letters,
            len(self.x_letters) > 0 (not all X letters used in guess).

        Returns: None.
        '''
        i = 0
        while i < 5:
            if self.sequence[i] != '-' and self.sequence[i] != guess[i]:
                raise exceptions.HardModeRule(
                    'Guess did not follow established sequence.'
                )
            i += 1
        
        i = 0
        while i < 5:
            if guess[i] in self.x_letters:
                self.x_letters.pop(self.x_letters.index(guess[i]))
            i += 1
        if len(self.x_letters) > 0:
            raise exceptions.HardModeRule('Not all X letters used.')