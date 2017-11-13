from __future__ import print_function

from cmd import Cmd
from collections import defaultdict

import sndhdr
import os
import shlex
import argparse

class Command(object):
    """ Command object """
    def __init__(self, name, logging=False):
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

    def call(self, args):
        for f in self.filelist:
            if not args.a:
                print(f + '\n')
            else:
                try:
                    if isinstance(sndhdr.what(f), sndhdr.SndHeaders):
                        print(f + '\n')
                except:
                    pass

class LookCommand(Command):
    def __init__(self, name, logging):
        super('look', logging)

    @property
    def cached_tree(self):
        return None

    def call(self, args):
        level = args.l

        if level > 0:
            walk_path = '.'
        elif level < 0:
            walk_path = '/'.join(['..'] * level)
        else:
            print("Can't walk 0 levels")

        depth = os.path.abspath(walk_path).count(os.path.sep)

        for root, dirs, files in os.walk(walk_path):
            yield root, dirs, files

            depth_from_root = root.count(os.path.sep)

            if depth + abs(level) <= depth_from_root:
                del dirs[:]

class UpdateCommand(Command):
    def __init__(self, name, logging):
        super('update', logging)

    @property
    def playlists(self):
        if self._playlists is None:
            self._playlists = defaultdict(list)

        return self._playlists

    def call(self, args):
        playlist, track = args.p, args.t

        if not track:
            self.playlists[playlist]
        else:
            if args.a:
                self.playlists[playlist].append(track)
            else:
                try:
                    self.playlists[playlist].remove(track)
                except ValueError:
                    pass

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

        self.playlists = defaultdict(list)

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
        print('LIST')

    def _do_update(self, args):
        print('update')

    def _do_look(self, args):
        print("LOOK")
        # if args.d and args.u:
        #     print(*utils.enqueue_tree(args.d), sep='\n')
        #     print(*utils.enqueue_tree(args.u, down=False), sep='\n')
        # elif args.d:
        #     print(*utils.enqueue_tree(args.d), sep='\n')
        # elif args.u:
        #     print(*utils.enqueue_tree(args.u, down=False), sep='\n')
        # else:
        #     print("No args given")

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
