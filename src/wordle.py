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
    Checks each letter of guess against all letters in answer.
    Constructs outstr containing '-','X','O' if guess letter is
    missing, in wrong place, or correct.

    Returns outstr.
    '''
    outstr = '.....'
    guess_i = 0
    while guess_i < len(guess):
        action_taken = False
        guess_letter = guess[guess_i]
        answer_i = 0
        while answer_i < len(answer):
            answer_letter = answer[answer_i]
            if guess_letter == answer_letter:
                    if guess_i == answer_i:
                        action_taken = True
                        outstr = splice_str(outstr,'O',guess_i)
                        guess = splice_str(guess,'_',guess_i)
                        answer = splice_str(answer,'_',guess_i)
                        break
                    else:
                        future_guess_letters = guess[guess_i+1:]
                        future_match = False
                        if guess_letter in future_guess_letters: # double letter in guess, check both
                            guess_j = guess_i+1
                            while guess_j < len(guess):
                                if guess[guess_j] == answer[guess_j]:
                                    future_match = True
                                    outstr = splice_str(outstr,'O',guess_j)
                                    outstr = splice_str(outstr,'-',guess_i)
                                    guess = splice_str(guess,'_',guess_j)
                                    answer = splice_str(answer,'_',guess_j)
                                    action_taken = True
                                    break
                                guess_j += 1
                            if not future_match:
                                outstr = splice_str(outstr,'X',guess_i)
                                guess = splice_str(guess,'_',guess_i)
                                answer = splice_str(answer,'_',answer_i)
                                action_taken = True
                                break
                            answer_i += 1
                            continue
                        else:
                            outstr = splice_str(outstr,'X',guess_i)
                            action_taken = True
                            break   
        
            answer_i += 1
        
        if not action_taken:
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
            filedate = line_list[0] + ' ' + line_list[1] + ' ' + line_list[2]
            if filedate == wordle_date:
                wordle = line_list[-1]

    if not wordle:
        input('Error reading wordle. Today\'s date not found.')
        sys.exit()
    
    return wordle

def main():
    import time

    wordle = read_wordle(resource_path('wordle_list.txt'))

    print('\n'+'*'*75)
    print("Welcome to Nick's Wordle clone! Try to guess the word!\n\
This clone replicates Josh Wardle\'s original game.\n\
It loads a new wordle from his original list every day, \n\
and is playable until October 20, 2027.\n\n\
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
        print('You won!')
    else:
        print(f'You lost. The word was {wordle}.')
    
    time.sleep(2)
    input('\nSee you tomorrow!')
    sys.exit()

if __name__ == '__main__':
    main()