'''Evaluates guess against solution word.'''

from collections import Counter

import str_utils 

STARTING_OUTSTR = '-----'

def evaluate_guess(guess, answer, valid_letters):
    '''Evaluates guess against solution word.

    Inputs:
    - guess (str): User's guess at the solution
    - answer (str): The solution word.

    Returns: Evaluation string (str), e.g., 'O X - O X'
    '''
    outstr = STARTING_OUTSTR
    letters_in_solution = Counter(answer)

    i = 0
    while i < 5:
        letter = guess[i]
        if letter == answer[i]:
            outstr = str_utils.splice_str(outstr, 'O', i)
            letters_in_solution[letter] -= 1
        i += 1

    i = 0
    while i < 5:
        letter = guess[i]
        if outstr[i] == "-" and letters_in_solution[letter] > 0:
            outstr = str_utils.splice_str(outstr, 'X', i)
            letters_in_solution[letter] -= 1
        i += 1

    i = 0
    while i < 5:
        if outstr[i] == '-':
            valid_letters.remove(guess[i])    
        i += 1

    return str_utils.pad_str(outstr).strip()