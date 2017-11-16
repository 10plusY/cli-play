from __future__ import print_function

from cmd import Cmd
from collections import defaultdict

import sndhdr
import os
import shlex
import argparse

class ArgDict(object):
    def __init__(self, args_ns, needed):
        self.args_ns = args_ns
        self.needed = needed

    def get_arg_dict(self, arg_ns, needed):
        if not isinstance(arg_ns, argparse.Namespace):
            raise Exception("Not an arg namespace.")
        else:
            config = {}
            for arg in needed:
                config[arg] = getattr(arg_ns, arg) or ''

            return config

    @property
    def dict(self):
        return self.get_arg_dict(self.arg_ns, self.needed)


class Command(object):
    """ Command object """
    def __init__(self, name, logging):
        self.name = name
        self.logging = logging

    def call(self, args):
        raise NotImplemented("Command call must be implemented.")

# Organize the commands based on the data structures they manipulate.

class ListCommand(Command):
    def __init__(self, name, logging):
        super('list', logging)

    @property
    def filelist(self):
        if self._filelist is None:
            self._filelist = os.listdir(os.getcwd())

        return self._filelist

    def list(self, audio=None):
        for f in self.filelist:
            if not audio:
                print(f + '\n')
            else:
                try:
                    if isinstance(sndhdr.what(f), sndhdr.SndHeaders):
                        print(f + '\n')
                except:
                    pass

    def call(self, args):
        self.list(args.a)

class LookCommand(Command):
    def __init__(self, name, logging):
        super('look', logging)

    @property
    def cached_tree(self):
        """
        Saves the tree audio files from each call.
        Appends new levels at each call.
        """
        return None

    def look(self, level):
        if level > 0:
            walk_path = '.'
        elif level < 0:
            walk_path = '/'.join(['..'] * level)
        else:
            return

        depth = os.path.abspath(walk_path).count(os.path.sep)

        for root, dirs, files in os.walk(walk_path):
            yield root, dirs, files

            depth_from_root = root.count(os.path.sep)

            if depth + abs(level) <= depth_from_root:
                del dirs[:]

    def call(self, args):
        self.look(args.l)

class UpdateCommand(Command):
    def __init__(self, name, logging):
        super('update', logging)

    @property
    def playlists(self):
        if self._playlists is None:
            self._playlists = defaultdict(list)

        return self._playlists

    def update(self, playlist, track, remove):
        if not track:
            self.playlists[playlist]
        else:
            if not remove:
                self.playlists[playlist].append(track)
            else:
                try:
                    self.playlists[playlist].remove(track)
                except ValueError:
                    pass

    def call(self, args):
        self.update(args.p, args.t, args.r)

# COMMAND LIST

class CommandList(object):
    """ Command list object """
    @property
    def commands(self):
        if self._commands is None:
            self._commands = []

            for atr in dir(self):
                if callable(getattr(self, atr)):
                    self._commands.append(atr)

            for call in self._commands:
                if call.startswith('__'):
                    self._commands.append(call)

        return self._commands

    def list(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def look(self):
        pass

class CliPlay(Cmd):

    def __init__(self, **kwargs):
        Cmd.__init__(self, **kwargs)

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers()

        self.register_list_parser(subparsers)
        self.register_add_parser(subparsers)
        self.register_remove_parser(subparsers)
        self.register_look_parser(subparsers)

    def register_list_parser(self, sub):
        list_parser = sub.add_parser("list")
        list_parser.add_argument("-a", action="store_true")
        list_parser.set_defaults(func=self._do_list)

    def register_add_parser(self, sub):
        add_parser = sub.add_parser("add")
        add_parser.add_argument("-p", required=True)
        add_parser.add_argument("-t", nargs='*')
        add_parser.set_defaults(func=self._do_add)

    def register_remove_parser(self, sub):
        remove_parser = sub.add_parser("remove")
        remove_parser.add_argument("-p", required=True)
        remove_parser.add_argument("-t", nargs='*')
        remove_parser.set_defaults(func=self._do_remove)

    def register_look_parser(self, sub):
        look_parser = sub.add_parser("look")
        look_parser.add_argument("-u", type=int)
        look_parser.add_argument("-d", type=int)
        look_parser.set_defaults(func=self._do_look)

    def preloop(self):
        self.intro = 'WELCOME TO CLI PLAY\n'
        self.prompt = '(Folder: {}): '.format(os.path.basename(os.getcwd()))

    def _do_list(self, args):
        print('***LIST***')

    def _do_look(self, args):
        print('***LOOK***')

    def _do_update(self, args):
        print('***UPDATE***')

    def do_quit(self, args):
        print("Shutting down...")
        raise SystemExit

    def default(self, line):
        args = self.parser.parse_args(shlex.split(line))

        try:
            args.func(args)
        except:
            Cmd.default(self, line)

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
