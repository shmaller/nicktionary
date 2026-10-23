'''Dictionary check for guesses; utility to split Webster's dictionary 
into separate files by first letter for faster use when checking guesses.

Webster's dictionary in JSON format downloaded from here:
https://github.com/matthewreagan/WebstersEnglishDictionary
'''

import os
import json

import fileops

ALPHABET = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

def in_dictionary(guess):
    '''Checks if guess in dictionary.

    Inputs: guess (str)

    Returns: True if guess in dictionary, False otherwise.
    '''
    dictionary = _load_dictionary(guess)
    if guess not in dictionary:
        return False
    return True

def _load_dictionary(guess):
    '''Load from json file the dictionary starting with the same letter 
    as the guess.

    Inputs: guess (str): Guess to check.

    Returns: dictionary (dict): Dictionary with keys of all words starting
        with same letter as guess.
    '''
    for letter in ALPHABET:
        if guess.startswith(letter):
            cwd = fileops.get_path(__file__)
            with open(f'{cwd}/dictionaries/{letter}.json') as f:
                return json.load(f)

# -----
# -- One-time use utility functions to build the game's dictionary. -----
# -----
    
def create_dictionary_jsons():
    '''One-time use utility to split Webster's dictionary into 
    sub-dictionaries of five-letter words, one file for each letter
    of the alphabet.'''
    five = _take_five('dictionary.json')
    _clear_definitions(five)
    _add_wordles(five)
    _split_by_letter(five)

def _take_five(dictionary_json):
    '''Cuts the dictionary down to five-letter words only.'''
    with open('dictionary.json') as f:
        english = json.load(f)
    five = {}
    for word in english:
        if len(word) == 5:
            five[word] = None

    return five

def _clear_definitions(dictionary):
    '''Remove definition data from dictionary - we just care about 
    the spelling of the word.
    '''
    for word in dictionary:
        dictionary[word] = None
        print(f'{word} now {dictionary[word]}')

def _add_wordles(dictionary):
    '''Some solution words are not in this dictionary. Add them.'''
    wordles = fileops.get_all_wordles()
    for word in wordles:
        dictionary[word] = None

def _split_by_letter(full_dictionary):
    '''Given a full dictionary, splits into one file per letter of the alphabet.

    Inputs: full_dictionary (dict): English dictionary.

    Returns: None.
    '''
    for letter in ALPHABET:
        json_obj = {}
        for entry in full_dictionary:
            word = entry.upper()
            if word.startswith(letter):
                json_obj[word] = None
        os.makedirs('dictionaries', exist_ok=True)
        with open(f'dictionaries/{letter}.json', 'w') as f:
            json.dump(json_obj, f, indent=2)

def check_solutions_against_dictionary():
    '''One-time use utility to make sure all solution words appear 
    in the chosen dictionary.
    '''
    cwd = fileops.get_path(__file__)
    with open(f'{cwd}/wordle_list.txt') as f:
        lines = f.readlines()
        print(f'{len(lines)} lines read')
    not_in = 0
    for line in lines:
        word = line.split()[-1]
        # print(f'Word: {word}')
        if not in_dictionary(word):
            not_in += 1
            print(f'{word} not found in dictionary. #{not_in}')

def expand_dictionary(words_file):
    with open(words_file) as f:
        lines = f.readlines()
    for letter in ALPHABET:
        dict_file = f'dictionaries/{letter}.json'
        with open(dict_file) as f:
            dic = json.load(f)
        for line in lines:
            word = line.upper().strip()
            first_letter = word[0]
            if first_letter == letter:
                if word not in dic:
                    print(f'Adding {word} to {first_letter}.json')
                    dic[word] = None
        with open(dict_file, 'w') as f:
            json.dump(dic, f, indent=2)
