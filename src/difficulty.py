import os
import json
import time
from pathlib import Path

class Difficulty:
    def __init__(self):
        self.filepath = Path(__file__).resolve().parent/'settings.json'

        if os.path.exists(self.filepath):
            self._load()
        else:
            self.mode = 'NORMAL'
            self._save()

    def _to_dict(self):
        return {'mode': self.mode}

    def _save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._to_dict(), f, indent=4)

    def _load(self):
        with open(self.filepath) as f:
            obj = json.load(f)

        self.mode = obj['mode']
        
    def change_mode(self):
        new_mode = input("'NORMAL' or 'HARD': ").upper().strip()
        if not new_mode in ['NORMAL', 'HARD']:
            print('Invalid game mode.')
            return self.change_mode()

        self.mode = new_mode
        self._save()

        outstr = f'\nNow playing {self.mode} mode.'
        if new_mode == 'HARD':
            outstr += ' Good luck!'
        print(outstr)
        time.sleep(1.25)