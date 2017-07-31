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

ACTION_TREE = {
    'list': {
		'audio': ,
        ''
	},
    'add': {
        '': ''
    }
}

def get_arg_response(action, arg):
    response = ACTION_TREE.get(action, None)
    return response


class CliPlay(Cmd):
    # Init
    def __init__(self):
        """ Shell params set here """

        Cmd.__init__(self)

        self.workinglist = []

    # Attrs
    def set_prompt(self, prompt):
        self.prompt = prompt

    def add_to_workinglist(self, fname):
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

        if args:
            for arg in args.split(' '):
                response = get_arg_response('list', arg)
                audio_files = filter_audio_files(flist)
                if list(audio_files):
                    print(*audio_files, sep='\n')
                else:
                    print(response['error'])
        else:
            filter_audio_files(*flist, sep='\n')

    def do_add(self, args):
        # Want to check if its in the cache
        flist = get_dir_cache()
        aflist = list(filter_audio_files(flist))

        if args:
            for arg in args.split(' '):
                if arg == 'add':
                    pass
                elif arg in aflist:





                response = get_arg_response('add', arg)
                audio_files = filter_audio_files(flist)




    def do_quit(self, args):
        """ Generic quit function for now """

        print("Shutting down...")

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
