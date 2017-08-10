from __future__ import print_function

from cmd import Cmd
from collections import defaultdict
from io import BytesIO

import sndhdr
import sys
import os
import re
import shlex
import argparse

CACHE = None

HDR_NO_HEADER = 'None'
HDR_RECURSING = 'recursing down:'
HDR_DIRECTORY = '*** directory (use -r) ***'

CLI_INTRO = 'WELCOME TO CLI PLAY\n'

BAD_HDR_TESTS = (HDR_NO_HEADER, HDR_RECURSING, HDR_DIRECTORY)

def prompt_string():
    """ Default is cwd base """
    return '(Folder: {}): '.format(os.path.basename(os.getcwd()))

def get_dir_cache():
    """ Return cache or redo dir listing """
    return CACHE or os.listdir(os.getcwd())

def hdr_to_audio_list():
    """ Returns list of audio files using the hdrtests """
    mainout = sys.stdout

    stream = BytesIO()

    sys.stdout = stream
    sndhdr.test()

    sys.stdout = mainout
    resultlist = stream.getvalue().split('\n')
    files = []

    for res in [_ for _ in resultlist if _]:
        name, test = res.split(": ")
        if test not in BAD_HDR_TESTS:
            files.append(name.strip('./'))

    return files

class CliPlay(Cmd):
    def __init__(self, **kwargs):
        Cmd.__init__(self, **kwargs)

        self.playlists = defaultdict(list)

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers()

        self.register_list_parser(subparsers)
        self.register_add_parser(subparsers)
        self.register_remove_parser(subparsers)
        self.register_move_parser(subparsers)

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

    def register_move_parser(self, sub):
        move_parser = sub.add_parser("move")
        move_parser.add_argument("-u", action="store_true")
        move_parser.add_argument("-d", action="store_true")
        move_parser.set_defaults(func=self._do_move)

    def preloop(self):
        self.intro = CLI_INTRO
        self.prompt = prompt_string()

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
            print("Can't remove%splaylist %s. Doesn't exist..." % ((" tracks %s from " % ', '.join(args.t)) if args.t else " ", args.p))
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

    # LOOK UP...LOOK DOWN
    def _do_move(self, args):
        if args.u and args.d:
            # TODO: Raise error
            print("Cannot move up and down...")
        elif args.u:
            print("Up")
        elif args.d:
            print("Down")
        else:
            print("Moyes")

    def do_quit(self, args):
        print("Shutting down...")
        raise SystemExit

    def default(self, line):
        args = self.parser.parse_args(shlex.split(line))

        try:
            args.func(args)
        except:
            Cmd.default(self, line)

play = CliPlay()
play.cmdloop()
