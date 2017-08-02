from __future__ import print_function

from cmd import Cmd

import os
import sndhdr
import sys
from IO import StringIO

cache = None

def get_prompt_string():
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
    mainout = sys.stdout

    stream = StringIO()

    sys.stdout = stream
    sndhdr.test()

    sys.stdout = mainout
    resultlist = stream.getvalue().split('\n')
    audiofiles = []

    for res in [_ for _ in resultlist if _]:
        name, test = res.split(": ", maxsplit=1)
        if test.startswith("SndHeaders"):
            audiofiles.append(name)

    return audiofiles

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
        self.set_prompt(get_prompt_string())

    def postloop(self):
        pass

    # Do Methods
    def do_list(self, args):
        """ """
        # Need Decorator
        flist = get_dir_cache()

        action = ACTION_TREE['list']
        if args:
            for arg in args.split(' '):
                try:
                    response = action[arg]
                    audio_files = filter_audio_files(flist)

                    if list(audio_files):
                        print(*audio_files, sep='\n')
                    else:
                        print(response['failure'])
                except:
                    pass
        else:
            action['default']['success'](flist)

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
