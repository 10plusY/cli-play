from __future__ import print_function

from cmd import Cmd

import os
import sndhdr
import sys
from io import BytesIO

cache = None

HDR_NO_HEADER = 'None'
HDR_RECURSING = 'recursing down:'
HDR_DIRECTORY = '*** directory (use -r) ***'

BAD_HDR_TESTS = (HDR_NO_HEADER, HDR_RECURSING, HDR_DIRECTORY)


def prompt_string():
    """ Default is cwd base """
    return '(Folder: {}): '.format(os.path.basename(os.getcwd()))

def get_dir_cache():
    """ Return cache or redo dir listing.
        Allows generator use.
    """
    return cache or os.listdir(os.getcwd())

def filter_audio_files(flist):
    for fname in flist:
        try:
            if sndhdr.what(fname):
                yield fname

        # Issues with directories - just skip it
        except:
            pass

def log_list(flist):
    print(*flist, sep='\n')

ACTION_TREE = {
    'list': {
        'default' : {
            'success': log_list
        },
        'audio': {
            'success': log_list,
            'failure': 'No audio files here...'
        }
    },
    'add': {
        'success': 'was added!',
        'failure': 'Failed to add file...'
    }
}

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
    # Init
    def __init__(self):
        """ Shell params set here """

        Cmd.__init__(self)

        self.workinglist = []

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
        """ List files in dir """
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
        # Want to check if its in the cache
        # Separate files? Splice
        flist = get_dir_cache()

        if args:
            tokens = args.split(' ')
            if sndhdr.what(tokens[0]):
                # ADD MESSAGES
                print('Impromper format; {} is not a playlist'.format(tokens[0]))
            elif tokens[0] in self.playlists:

                self.playlists.extend(tokens[1:])
        else:
            print(ACTION_TREE['add']['failure'])

    def do_quit(self, args):
        """ Generic quit function for now """

        print("Shutting down...")

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
