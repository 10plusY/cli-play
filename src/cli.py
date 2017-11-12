from __future__ import print_function

from cmd import Cmd
from collections import defaultdict

import sndhdr
import sys
import os
import re
import shlex
import argparse

import utils

class Command(object):
    """ Command object """
    def __init__(self, name, logging=False):
        self.name = name
        self.logging = logging

    def call(args):
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

    def call(args):
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

    def call(args):
        pass

class UpdateCommand(Command):
    def __init__(self, name, logging):
        super('update', logging)

    @property
    def playlists(self):
        if self._playlists = None:
            self._playlists = defaultdict(list)

        return self._playlists

    def call(args):
        playlist, track = args.p, args.t

        new_entry = {playlist: None}

        try:
            current_playlist = self.playlists[playlist]
        except KeyError:
            new_entry[playlist] = []
        else:
            if arg.a:
                new_entry[playlist] = current_playlist.append(track)
            else:
                new_entry[playlist] = current_playlist.remove(track)
        finally:
            self.playlists[playlist].update(new_entry)


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
        if args.a:
            print(*hdr_to_audio_list(), sep='\n')
        else:
            print(*get_dir_cache(), sep='\n')

    def _do_add(self, args):
        if not args.t:
            if self.playlists.get(args.p) is None:
                print("Creating playlist %s..." % args.p)
                self.playlists[args.p]
            else:
                print("Playlist %s already exists..." % args.p)
        else:
            if self.playlists.get(args.p) is None:
                print("Creating playlist %s..." % args.p)

            new_entries = filter(lambda t: t not in self.playlists[args.p], args.t)
            new_tracks = filter(lambda t: t not in hdr_to_audio_list(), new_entries)

            print("Adding tracks %s to playlist %s" % ((', '.join(new_tracks), args.p)))

            if new_entries != new_tracks:
                print("Couldn't add tracks %s" % (', '.join(list(set(new_entries) - set(new_tracks)))))
                print("Not audio tracks...")

            self.playlists[args.p].extend(new_tracks)

    def _do_remove(self, args):
        if self.playlists.get(args.p) is None:
            print("Can't remove%splaylist %s. Doesn't exist..."
                    % ((" tracks %s from " % ', '.join(args.t)) if args.t else " ", args.p))
        elif args.t:
            for t in args.t:
                if t in self.playlists[args.p]:
                    print("Removing %s..." % t)
                    self.playlists[args.p].remove(t)
                else:
                    print("%s not in playlist...")
        else:
            print("Removing playlist %s..." % args.p)
            del self.playlists[args.p]

    def _do_look(self, args):
        if args.d and args.u:
            print(*utils.enqueue_tree(args.d), sep='\n')
            print(*utils.enqueue_tree(args.u, down=False), sep='\n')
        elif args.d:
            print(*utils.enqueue_tree(args.d), sep='\n')
        elif args.u:
            print(*utils.enqueue_tree(args.u, down=False), sep='\n')
        else:
            print("No args given")

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
