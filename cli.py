from cmd import Cmd

class CliPlay(Cmd):
    def __init__(self):
        """Shell params set here"""

        Cmd.__init__(self)

        self.intro = 'Welcome '
        self.prompt = '|> '

    def do_quit(self, args):
        """Generic quit function for now."""

        print "Shutting down..."

        raise SystemExit

if __name__ == '__main__':
    play = CliPlay()
    play.cmdloop()
