'''Tracked and sharable game stats.'''

import json
import datetime

class Stat:
    '''Stat object that tracks a single day's results.
    
    Inputs:
        date (datetime.date): Date for this stat
        guess_log (GuessLog): GuessLog object tracking evaluation by guess number.
    '''
    def __init__(self, date):
        self.date = date
        self.guess_count = 0
        self.eval_log = {}
        self.won = False

    def add_guess(self, guess_no, evaluation):
        self.eval_log[guess_no] = evaluation
        self.guess_count = len(self.eval_log)
        if evaluation == 'O O O O O':
            self.won = True

    def to_dict(self):
        return {
            'date': self.date,
            'guess_count': self.guess_count,
            'eval_log': self.eval_log,
            'won': self.won
        }

    def load(self, dict):
        try:
            self.date = dict['date']
            self.eval_log = dict['eval_log']
            self.won = dict['won']
            self.guess_count = len(self.eval_log)
        except KeyError:
            print('Error loading stat: data format not correct.')
    
    def print(self):
        outstr = ''
        for i in range(1,len(self.eval_log)):
            outstr += f'{i}: {self.eval_log[i]}'
