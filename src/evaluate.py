'''Evaluates guess against solution word.'''

from str_utils import splice_str

def evaluate_guess(guess,answer):
    '''Evaluates guess against solution word. Returns 

    Inputs:
    - guess (str): User's guess at the solution
    - answer (str): The solution word.

    Returns: Evaluation string (str), e.g., 'O X - O X'
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

    return outstr