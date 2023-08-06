def join_to_absolute_path(*args):
    import os

    return os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join(*args))))
