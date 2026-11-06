import os
import json
import time
from pathlib import Path

class Difficulty:
    '''Game difficulty: allows user to choose between NORMAL and HARD mode.
    Methods to save to and load from file, update game difficulty.
    '''
    def __init__(self):
        self.filepath = Path(__file__).resolve().parent/'settings.json'

        if os.path.exists(self.filepath):
            self._load()
        else:
            self.mode = 'NORMAL'
            self._save()

    def _to_dict(self):
        '''Convert self to dictionary to save to JSON.

        Inputs: None.

        Returns: dict[str, str]: {'mode': self.mode}
        '''
        return {'mode': self.mode}

    def _save(self):
        '''Saves dict version of self to JSON file.

        Inputs: None.

        Returns: None.
        '''
        with open(self.filepath, 'w') as f:
            json.dump(self._to_dict(), f, indent=4)

    def _load(self):
        '''Loads settings from JSON file.

        Inputs: None.

        Returns: None.
        '''
        with open(self.filepath) as f:
            obj = json.load(f)

        self.mode = obj['mode']
        
    def change_mode(self):
        '''Prompts user input for new difficulty, updates and saves to JSON.

        Inputs: None.

        Returns: None.
        '''
        print(f"\nYou're currently playing {self.mode} mode.")
        new_mode = input("Select your game difficulty (NORMAL/HARD): ").upper().strip()
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