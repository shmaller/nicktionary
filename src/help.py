'''Launches the tutorial.'''

import webbrowser

import fileops

def help():
    '''Launches help webpage with default browser.

    Inputs: None.

    Returns: None.
    '''
    current_path = fileops.get_path(__file__)
    uri = fileops.get_uri(f'{current_path}/help.html')
    webbrowser.open(uri)