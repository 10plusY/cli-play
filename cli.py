from cmd import Cmd

import os

cache = []

def get_prompt_string():
    """ Default is cwd base """
    return '(Folder: {}): '.format(os.path.basename(os.getcwd()))

def get_dir_cache():
    return cache or os.listdir(os.getcwd())

class CliPlay(Cmd):
    # Init
    def __init__(self):
        """ Shell params set here """

        Cmd.__init__(self)

        self.intro = 'WELCOME TO CLI-PLAY\n'

    # Attrs
    def set_prompt(self, prompt):
        self.prompt = prompt

    # Hooks
    def preloop(self):
        self.set_prompt(get_prompt_string())

    def postloop(self):
        pass


    # Do Methods
    def do_list(self, args):
        """ """
        for item in get_dir_cache():
            print item


    def do_quit(self, args):
        """ Generic quit function for now """

        print "Shutting down..."

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
