from dictionary import ALPHABET

class ValidLetters:
    '''Container class which tells the user which letters have and have not
    yet been eliminated by their guesses.

    Inputs: None.
    '''
    def __init__(self):
        self.letters = ALPHABET.copy()
        self.eliminated = []

    def remove(self, letter):
        '''Remove a guess from the valid list. This should correspond 
        to a letter which has gotten a '-' evaluation from evaluate.evaluate().

        Removes from self.letters, adds to self.eliminated, sorts 
        self.eliminated alphabetically.

        Inputs:
        - letter (str): Letter to remove.

        Returns: None.
        '''
        try:
            i = self.letters.index(letter)
            del self.letters[i]
        except ValueError:
            return

        self.eliminated.append(letter)
        self.eliminated.sort()