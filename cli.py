from cmd import Cmd

import os

def get_prompt_string():
    return '(Folder: {} )'.format(os.path.basename(os.getcwd()))

class CliPlay(Cmd):
    # Init
    def __init__(self):
        """Shell params set here"""

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
    def do_quit(self, args):
        """Generic quit function for now."""

        print "Shutting down..."

        raise SystemExit

    # Help Methods

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
