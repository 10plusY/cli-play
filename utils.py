import os

from collections import deque

def walk_by_level(path, level):
    """

        Walks the file system up to a certain level/depth

        i.e. For a directory tree

        -- /
            -- Foo
            -- Bar
                -- Qux
                    -- Quux
                    -- Corge

        walk_by_level('/', 2) returns ('/', '/Foo', '/Bar', '/Bar/Qux')

        :param path - path to form the root of the tree
        :param level - number of steps to go down the tree

    """
    path = os.path.abspath(path)

    current_depth = path.count(os.path.sep)

    for root, dirs, files in os.walk(path):
        yield root, dirs, files

        root_depth = root.count(os.path.sep)

        if current_depth + level <= root_depth:
            del dirs[:]

def walk_down(level):
    """

        Walks downwards to certain level

        :param level - number of steps to go down the tree

    """
    return walk_by_level('.', level)

def walk_up(level):
    """

        Walks downwards but first moves the root of the tree
        a certain level up

        :param level - number of steps to go down the tree

    """
    return walk_by_level('/'.join(['..'] * level), level)

def look_tree(level):
    """
        Returns level tree starting up or down based on the parity
        of the level.

        :param level - signed number of steps to walk the tree
    """
    if level > 0:
        return walk_up(abs(level))
    elif level < 0:
        return walk_down(abs(level))
    else:
        pass

def enqeue_tree(level):
    """
        Takes signed level and returns a queue with the files
        in the tree in the appropriate direction

        :param level - signed number of steps to walk the tree (+ down/- up)
    """
    queue = deque()

    tree = look_tree(level)

    if level > 0:
        for root, dirs, files in tree:
            queue.append(root)
    elif level < 0:
        for root, dirs, files in tree:
            queue.appendleft(root)
    else:
        pass

    return queue
