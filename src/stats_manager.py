import json

import fileops
import str_utils
from game_stat import Stat

CURRENT_PATH = fileops.get_path(__file__)

class StatsManager:
    '''Container class that holds and manages many game_stat.Stat
    objects. Loads stats from stats.json; creates that file 
    if it does not exist.

    Inputs: None.
    '''
    def __init__(self):
        self.stats = {}
        self.filename = f'{CURRENT_PATH}/stats.json'
        try:
            self._load(self.filename)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print('No user stats found, starting new stats count.')
            self.save()
                
    def _load(self, filename):
        '''Load a JSON file with stats data keyed by stat date.
        For each date, create a Stat object and store it in self.stats.

        Inputs:
            - filename (str): Filename to load.

        Returns: None.
        '''
        with open(filename) as f:
            obj = json.load(f)
        for stat_date in obj:
            stat = Stat(stat_date)
            stat.load(obj[stat_date])
            self.stats[stat_date] = stat

    def save(self, filename='stats.json'):
        '''Save stats log to JSON file in current directory.

        Inputs:
            - filename (str) (optional): Filename to save.

        Returns: None.
        '''
        with open(f'{CURRENT_PATH}/{filename}', 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def add_stat(self, stat):
        '''Add a new game_stat.Stat object to storage dictionary.

        Inputs:
            - stat (game_stat.Stat): Stat object representing single game play

        Returns: None.
        '''
        self.stats[stat.date] = stat

    def to_dict(self):
        '''Convert self to dictionary to save to JSON.

        Inputs: None.

        Returns: Dictionary of stats keyed by stat date.
        '''
        stats_dict = {}
        for stat_date in self.stats:
            stat = self.stats[stat_date]
            stats_dict[stat_date] = stat.to_dict()

        return stats_dict

    def count_user_stats(self):
        return len(self.stats)
        '''Generate metrics for stats: how many wins/losses, 
        how many guesses it has taken to win the game, 
        how many times played overall.

        Inputs: None.

        Returns: Dictionary with keys 'won', 'lost', 1-6.
        '''
        guess_breakdown = {'won': 0, 'lost': 0}
        for stat_date in self.stats:
            stat = self.stats[stat_date]
            if stat.won:
                guess_breakdown['won'] += 1
            else:
                guess_breakdown['lost'] += 1
            for i in range(1,7):
                if stat.guess_count == i:
                    if i in guess_breakdown:
                        guess_breakdown[i] += 1
                    else:
                        guess_breakdown[i] = 1
        for i in range(1,7):
            if not i in guess_breakdown:
                guess_breakdown[i] = 0

        return guess_breakdown

    def today(self):
        date = datetime.date.today().strftime('%D')
        try:
            return self.stats[date]
        except KeyError:
            print("Looks like you haven't played yet today.")
            return None
    
    def display(self):
        bd = self.gen_stats_breakdown()
        input(str_utils.gen_stats_breakdown_str(
            self.count_user_stats(), self.gen_stats_breakdown()
        ))
