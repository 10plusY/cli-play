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

        list_parser = subparsers.add_parser("list")
        list_parser.add_argument("-a", action='store_true')
        list_parser.set_defaults(func=self._do_list)

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("-p", nargs='?')
        add_parser.set_defaults(func=self._do_add)

    def _do_list(self, args):
        if args.a:
            print(*hdr_to_audio_list(), sep='\n')
        else:
            print(*get_dir_cache(), sep='\n')

    def _do_add(self, args):
        if args.p:
            self.playlists[args.p]
            print("New playlist %s created..." % args.p)
        else:
            print("No playlist...")

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



# class CliPlay(Cmd):
#     """ Object representing the command line tool playlist creator """
#     def __init__(self):
#         """ Shell params set here """
#
#         Cmd.__init__(self)
#
#         self._playlists = defaultdict(list)
#
#     def get_playlists(self):
#         return self.playlists
#
#     # Attrs
#     def set_prompt(self, prompt):
#         self.prompt = prompt
#
#     # Hooks
#     def preloop(self):
#         self.intro = 'WELCOME TO CLI-PLAY\n'
#         self.set_prompt(prompt_string())
#
#     # CLI Methods
#     def do_list(self, arg):
#         """ List files in dir
#
#             :param args - arg string
#         """
#         if arg and arg == '-a':
#             audiolist = hdr_to_audio_list()
#
#             if audiolist:
#                 print(*audiolist, sep='\n')
#             else:
#                 print('No audio files in this dir...')
#
#             return
#
#         print(*get_dir_cache(), sep='\n')
#
#     def do_add(self, args):
#         if args:
#             pass
#         else:
#             print("No playlist/tracks specificied. Cannot add...")
#
#     def do_quit(self, args):
#         """ Generic quit function for now """
#
#         print("Shutting down...")
#
#         raise SystemExit
#
#     # Help Methods
#
# play = CliPlay()
# play.cmdloop()
