"""Methods to work on file systems."""


import os


def find(path, extensions = None, recurse = True, n_max = None):
    """Get list of paths to files in a folder.
    
    Args:
        path (str): Path to a folder on a filesystem.
        extensions
    
    """
    file_list = []
    if extensions is not None:
        tmp = []
        for e in extensions:
            e = str(e).lower()
            if not e.startswith("."):
                e = f".{e}"
            tmp.append(e)
        extensions = tmp
    i = 0
    for root, dirs, files in os.walk(path):
        if n_max is not None and i >= n_max:
            break
        for name in files:
            if extensions is not None:
                ext = os.path.splitext(name)[1]
                if ext.lower() not in extensions:
                    continue
            i += 1
            file_list.append(os.path.join(root, name))
            if n_max is not None and i >= n_max:
                break
    return file_list

