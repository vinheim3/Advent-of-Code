import os


def get_fname(filepath):
    script_dir = os.path.dirname(filepath)
    return os.path.join(script_dir, 'input.txt')
