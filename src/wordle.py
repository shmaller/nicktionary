'''
Wordle clone
Nicholas Boni
December 12, 2023
'''
import os, sys

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
    There is still a bug where, if a guess has duplicate letters,
    one of which starts the guess,
    one of which exists later in the solution,
    it will leave the first result as '.' in the outstr
    '''
    outstr = '.....'
    guess_i = 0
    while guess_i < len(guess):
        action_taken = False
        guess_letter = guess[guess_i]
        # print(f'Guess letter: {guess_letter}')
        answer_i = 0
        while answer_i < len(answer):
            answer_letter = answer[answer_i]
            # print(f'Answer letter: {answer_letter}')
            if guess_letter == answer_letter:
#                     print(f'Guess letter {guess_letter} at guess position {guess_i} \
# # matches answer letter {answer_letter} at answer position {answer_i}. Investigating...')
                    if guess_i == answer_i:
                        action_taken = True
                        outstr = splice_str(outstr,'O',guess_i)
                        guess = splice_str(guess,'_',guess_i)
                        answer = splice_str(answer,'_',guess_i)
#                         print(f'O result. outstr now looks like this: {outstr}\
# guess now looks like this: {guess}\
# answer now looks like this: {answer}')
                        break
                    else:
                        # print('The positions do not match. Not an O.')
                        # print('Checking for double letters in guess.')
                        future_guess_letters = guess[guess_i+1:]
                        # print(f'Remaining letters in guess: {future_guess_letters}')
                        future_match = False
                        if guess_letter in future_guess_letters: # double letter in guess, check both
#                             print('There is another instance of this letter in future guess letters.\
# Checking if that one is correct.')
                            guess_j = guess_i+1
                            while guess_j < len(guess):
#                                 print(f'Checking future guess letter {guess[guess_j]} for a match \
# with future answer letter {answer[guess_j]}')
                                if guess[guess_j] == answer[guess_j]:
                                    # print('There is a future match.')
                                    future_match = True
                                    outstr = splice_str(outstr,'O',guess_j)
                                    outstr = splice_str(outstr,'-',guess_i)
                                    # print(f'outstr now looks like this: {outstr}')
                                    guess = splice_str(guess,'_',guess_j)
                                    answer = splice_str(answer,'_',guess_j)
                                    # print(f'guess now this: {guess}')
                                    # print(f'answer now this: {answer}')
                                    action_taken = True
                                    # guess_i = answer_i = 0
                                    break
                                guess_j += 1
                            if not future_match:
                                # print('No future match. Its an X.')
                                # print(f'inserting X to position {guess_i} in outstr')
                                outstr = splice_str(outstr,'X',guess_i)
                                guess = splice_str(guess,'_',guess_i)
                                answer = splice_str(answer,'_',answer_i)
                                # print(f'outstr: {outstr}')
                                action_taken = True
                                break
                            answer_i += 1
                            continue
                        else:
                            # print('No repeated letters. Its an X.')
                            outstr = splice_str(outstr,'X',guess_i)
                            action_taken = True
                            break   
        
            answer_i += 1
        
        if not action_taken:
            # print('Letter not found.')
            outstr = splice_str(outstr,'-',guess_i)
        
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
    if str[index:]:
        new_footer = str[index+1:]
    else:
        new_footer = ''
    # print(f'Splicing. New header: {new_header} New footer: {new_footer}')
    return new_header + new_footer

def read_wordle(infile):
    '''
    Accepts infile with list of all wordle solutions.

    Grabs today's date, scans infile for appropriate 
    wordle solution.

    Returns wordle solution as str.
    '''
    from datetime import date
    today = date.today()
    wordle_date = today.strftime('%b %d %Y')
    wordle = ''

    if not os.path.isfile(infile):
        print('\n'+'*'*75)
        print("ERROR: Cannot find solution list. \n\
Make sure 'wordle_list.txt' exists in the same \
directory as this program. \n\
Press ENTER to quit, place the file in this directory, \
and then try again.")
        print('*'*75)
        input()
        sys.exit()
    
    with open(infile) as f:
        for line in f:
            line_list = line.split()
            # print(line_list)
            filedate = line_list[0] + ' ' + line_list[1] + ' ' + line_list[2]
            # print(filedate)
            if filedate == wordle_date:
                wordle = line_list[-1]

    if not wordle:
        input('Error reading wordle. Today\'s date not found.')
        sys.exit()
    
    return wordle

def main():
    wordle = read_wordle(resource_path('wordle_list.txt'))

    print('\n'+'*'*75)
    print("Welcome to Nick's Wordle clone! Try to guess the word!\n\
This clone replicates Josh Wardle\'s original game.\n\
It follows his word list and is playable until October 20, 2027.\n\n\
HOW TO PLAY:\n\
Type a five-letter word and hit ENTER.\n\
The game will evaluate your guess.\n\
An 'O' means that this letter is in the right place.\n\
An 'X' means that this letter is in the solution, \n\
          but in a different place than you guessed.\n\
A '-' means that this letter does not appear in the solution.\n\
Type 'quit' at any time to end the game.")
    print('*'*75+'\n')

    i = 0
    won = False
    while i < 6 and not won:
        guess = input(f'GUESS #{i+1}: ').strip().upper()

        if guess == 'QUIT':
            sys.exit()
        if len(guess) != 5:
            print('Invalid guess!')
            continue
        if not guess.isalnum():
            input('Invalid guess!')
            continue

        outstr = evaluate_guess(guess,wordle)
        print(outstr)

        if outstr == 'OOOOO':
            won = True
            break
        i += 1
    
    if won:
        input('You won!')
    else:
        input(f'You lost. The word was {wordle}.')
    
    input('\nSee you tomorrow!')
    sys.exit()

if __name__ == '__main__':
    main()