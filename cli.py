from __future__ import print_function

from cmd import Cmd
from collections import defaultdict
from io import BytesIO

import sndhdr
import sys
import os

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
    """ Object representing the command line tool playlist creator """
    def __init__(self):
        """ Shell params set here """

        Cmd.__init__(self)

        self.workinglist = []
        self.playlists = defaultdict(list)

    def get_playlists(self):
        return self.playlists

    # Attrs
    def set_prompt(self, prompt):
        self.prompt = prompt

    def add_to_main_list(self, fname):
        self.workinglist.append(fname)

    # Hooks
    def preloop(self):
        self.intro = 'WELCOME TO CLI-PLAY\n'
        self.set_prompt(prompt_string())

    def postloop(self):
        pass

    # Do Methods
    def do_list(self, args):
        """ List files in dir

            :param args - arg string
        """
        if args:
            for arg in args.split(' '):
                if arg == 'audio':
                    audiolist = hdr_to_audio_list()

                    if audiolist:
                        print(*audiolist, sep='\n')
                    else:
                        print('Failed to add file...')
        else:
            print(*get_dir_cache(), sep='\n')

    def do_add(self, args):
        """ """
        if args:
            all_args = args.split(' ')
            first_arg = all_args.pop(0)
            other_args = all_args

            audiolist = hdr_to_audio_list()

            # If all of the args are audio, they can be added
            if all(_ in audiolist for _ in other_args):
                
                if self.get_playlists().get(first_arg) is None:
                    print("Creating playlist {}...".format(first_arg))

                self.playlists[first_arg].extend(other_args)
            else:
                audioargs = filter(lambda arg: arg in hdr_to_audio_list(), other_args)
                not_audiofiles = list(set(audioargs).symmetric_difference(set(other_args)))
                print("Add failed...\nFiles {} not added...".format(', '.join(not_audiofiles)))
        else:
            print("No playlist and argument given\nUsage: add <PLAYLIST> [TRACK1 TRACK2 ...]")

    def do_quit(self, args):
        """ Generic quit function for now """

        print("Shutting down...")

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
