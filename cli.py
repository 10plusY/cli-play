from cmd import Cmd

import os

class CliPlay(Cmd):
    def __init__(self):
        """Shell params set here"""

        Cmd.__init__(self)

        self.intro = 'WELCOME TO CLI-PLAY\n'

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_prompt(self):
        return '(Folder: {}) '.format(os.path.basename(os.getcwd()))

    def preloop(self):
        self.set_prompt(self.get_prompt())

    def do_quit(self, args):
        """Generic quit function for now."""

        print "Shutting down..."

        raise SystemExit

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
