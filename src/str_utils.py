'''String manipulation utilities.'''

import time

def pad_str(str):
    '''Pads str with internal spaces.

    Input: str (str): In string.

    Returns: str with spaces between each character.
    '''
    outstr = ''
    for char in str:
        outstr += char + ' '

    return outstr.strip()

def crawl(str):
    '''Crawls str across the screen slowly.

    Input: str (str): String to crawl.

    Returns None.
    '''
    for char in str:
        time.sleep(0.1)
        print(char,end='',flush=True)

def splice_str(str,letter,index):
    '''Inserts letter into str at index.

    Inputs:
    - str (str): String to insert letter into.
    - letter (str): Letter to insert into str.
    - index (int): Index in str at which to insert letter.

    Returns: Spliced string (str)
    '''
    new_header = str[0:index] + letter
    new_footer = ''

    if str[index:]:
        new_footer = str[index+1:]

    return new_header + new_footer