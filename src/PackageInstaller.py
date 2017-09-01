'''
Created on 01.09.2017

@author: henrik.pilz
'''
from subprocess import call

def __getPip():
    """
    Pip is the standard package manager for Python.
    This returns the path to the pip executable, installing it if necessary.
    """
    from os.path import isfile, join
    from sys     import prefix
    # Generate the path to where pip is or will be installed... this has been
    # tested and works on Windows, but will likely need tweaking for other OS's.
    # On OS X, I seem to have pip at /usr/local/bin/pip?
    pipPath = join(prefix, 'Scripts', 'pip.exe')

    # Check if pip is installed, and install it if it isn't.
    if not isfile(pipPath):
        raise("Failed to find or install pip!")
    return pipPath
    
def installIfNeeded(moduleName, nameOnPip=None, notes=""):
    """ Installs a Python library using pip, if it isn't already installed. """
    from pkgutil import iter_modules

    # Check if the module is installed
    if moduleName not in [tuple_[1] for tuple_ in iter_modules()]:
        print("Installing " + moduleName + notes + " Library for Python")
        call([__getPip(), "install", nameOnPip if nameOnPip else moduleName])