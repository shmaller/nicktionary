'''Launches the tutorial.'''

import os
import webbrowser
from pathlib import Path

def help():
    '''Launches help webpage with default browser.

    Inputs: None.

    Returns: None.
    '''
    uri = Path(_get_current_path(),'help.html').as_uri()
    webbrowser.open(uri)

def _get_current_path():
    '''Resolves source code filepath to launch help.html.

    Inputs: None.

    Returns: None.
    '''
    current_path = os.path.realpath(__file__)
    return os.path.dirname(current_path)