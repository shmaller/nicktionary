'''Launches the tutorial.'''

import os
import webbrowser

def help():
    '''Launches help webpage with default browser.

    Inputs: None.

    Returns: None.
    '''
    path = _get_current_path()
    webbrowser.open(f'{path}/help.html')

def _get_current_path():
    '''Resolves source code filepath to launch help.html.

    Inputs: None.

    Returns: None.
    '''
    current_path = os.path.realpath(__file__)
    return os.path.dirname(current_path)