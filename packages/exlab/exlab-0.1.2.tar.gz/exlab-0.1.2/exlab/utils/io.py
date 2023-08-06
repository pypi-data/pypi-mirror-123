from exlab.utils.structure import get_dict_path

import re
import os
import subprocess


def parameter(var, default=None):
    return var if var is not None else default


def shortid(instance, length=4):
    return str(id(instance))[-length:]


def mkdir(folder):
    """
    Creates the requested folder if it doesn't exist
    """
    os.makedirs(folder, exist_ok=True)


def emptydir(folder):
    """
    Empties the given folder
    """
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception:
            pass


def get_git_root(path):
    while not os.path.exists(os.path.join(path, '.git')):
        previouspath = path
        path = os.path.dirname(path)
        if path == previouspath or not os.path.exists(path):
            return None

    return path

def get_git_hash(path, tuple=True):
    path = get_git_root(path)
    if not path:
        return ''

    try:
        hash_ = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=path).decode('ascii').strip()
    except Exception:
        hash_ = 'unknown'

    return hash_


def get_git_hashes():
    """
    Get the get_commit_hash from the current git commit
    """
    from exlab.interface.loader import Loader
    return {os.path.basename(get_git_root(path)): get_git_hash(path) for path in Loader.instance().sourcepath if get_git_root(path)}


class Templater(object):
    def __init__(self, dict_={}):
        self.dict_ = dict_
    
    def render(self, data):
        def replace(match):
            try:
                return str(get_dict_path(self.dict_, match.group(1)))
            except KeyError:
                return 'unknown'
        
        return re.sub(r'{([\%\w\.]*)}', replace, data)
