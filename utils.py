import os

from collections import deque

def walk_level(path, level):
    path = os.path.abspath(path)

    current_depth = path.count(os.path.sep)

    for root, dirs, files in os.walk(path):
        yield root, dirs, files

        root_depth = root.count(os.path.sep)

        if current_depth + level <= root_depth:
            del dirs[:]
