import json
import textwrap

import fileops
import str_utils
from game_stat import Stat

CURRENT_PATH = fileops.get_path(__file__)

class StatsManager:
    def __init__(self):
        self.stats = {}
        self.filename = f'{CURRENT_PATH}/stats.json'
        try:
            self._load(self.filename)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print('No user stats found, starting new stats count.')
            self.save()
                
    def _load(self, filename):
        with open(filename) as f:
            obj = json.load(f)
        for stat_date in obj:
            stat = Stat(stat_date)
            stat.load(obj[stat_date])
            self.stats[stat_date] = stat

    def save(self, filename='stats.json'):
        with open(f'{CURRENT_PATH}/{filename}', 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def add_stat(self, stat):
        self.stats[stat.date] = stat

    def to_dict(self):
        stats_dict = {}
        for stat_date in self.stats:
            stat = self.stats[stat_date]
            stats_dict[stat_date] = stat.to_dict()

        return stats_dict

    def count_user_stats(self):
        return len(self.stats)
    
    def gen_stats_breakdown(self):
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
