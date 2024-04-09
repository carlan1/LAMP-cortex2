# recursive `from module import *` excluding anything prefixed with '_':
from importlib import import_module

import sys
import os

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the directory containing the current script
current_dir = os.path.dirname(current_script_path)

# Add the directory to sys.path if it's not already included
if current_dir not in sys.path:
    sys.path.append(current_dir)
    
import LAMP2

from pkgutil import walk_packages
for mod_info in walk_packages(__path__, __name__ + '.'):
    if mod_info.name.endswith('__main__'):
        continue
    mod = import_module(mod_info.name)
    try:
        names = mod.__dict__['__all__']
    except KeyError:
        names = [k for k in mod.__dict__ if not k.startswith('_')]
    globals().update({ k: getattr(mod, k) for k in names })