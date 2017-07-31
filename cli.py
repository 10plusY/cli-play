from __future__ import print_function

from cmd import Cmd

import os
import sndhdr

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

ARG_TREE = {
    'list': {'audio': {'action': filter_audio_files, 'error': 'No audio files in this directory...'}}
}

def get_arg_response(action, arg):
    response = ARG_TREE.get(action, None).get(arg, None)
    return response


class CliPlay(Cmd):
    # Init
    def __init__(self):
        """ Shell params set here """

        Cmd.__init__(self)

    # Attrs
    def set_prompt(self, prompt):
        self.prompt = prompt

    # Hooks
    def preloop(self):
        self.intro = 'WELCOME TO CLI-PLAY\n'
        self.set_prompt(get_prompt_string())

    def postloop(self):
        pass

    # Do Methods
    def do_list(self, args):
        """ """
        flist = get_dir_cache()

        def print_dir_list(l):
            for a in l:
                print(a)

        if args:
            for arg in args.split(' '):
                response = get_arg_response('list', arg)
                audio_files = filter_audio_files(flist)
                if list(audio_files):
                    print_dir_list(audio_files)
                else:
                    print(response['error'])
        else:
            print_dir_list(flist)

    def do_quit(self, args):
        """ Generic quit function for now """

        print("Shutting down...")

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
