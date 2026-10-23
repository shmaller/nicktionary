'''Tracked and sharable game stats.'''

class Stat:
    '''Stat object that tracks a single game's results.
    
    Inputs:
    - date (str): Date for this stat
    '''
    def __init__(self, date):
        self.date = date
        self.guess_count = 0
        self.eval_log = {}
        self.won = False

    def add_guess(self, guess_no, evaluation):
        '''Logs an individual guess.

        Inputs:
        - guess_no (int): Which guess this was in the sequence (1-6)
        - evaluation (str): Evaluation string for that guess (e.g., 'O X - - X')

        Returns: None.
        '''
        self.eval_log[guess_no] = evaluation
        self.guess_count = len(self.eval_log)
        if evaluation == 'O O O O O':
            self.won = True

    def to_dict(self):
        '''Converts self to dictionary for saving and export.

        Inputs: None.

        Returns: Dictionary version of self.
        '''
        return {
            'date': self.date,
            'guess_count': self.guess_count,
            'eval_log': self.eval_log,
            'won': self.won
        }

    def load(self, dict):
        '''Loads dictionary data into this object's attributes.

        Inputs:
        - dict (dict): Dictionary with keys 'date', 'eval_log', 'won'

        Returns: None.
        '''
        self.date = dict['date']
        self.eval_log = dict['eval_log']
        self.won = dict['won']
        self.guess_count = len(self.eval_log)
