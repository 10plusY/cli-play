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

        for hdr in filter_audio_files(flist):
            print hdr

    def do_quit(self, args):
        """ Generic quit function for now """

        print "Shutting down..."

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
