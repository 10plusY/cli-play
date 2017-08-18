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

def enqeue_tree(tree, down=True, queue=deque()):
    """

        Takes signed level and returns a queue with the files
        in the tree in the appropriate direction

        :param level - signed number of steps to walk the tree (+ down/- up)
        
    """
    if down:
        for root, dirs, files in tree:
            queue.append(root)
    else:
        for root, dirs, files in tree:
            queue.appendleft(root)

    return queue
