""" schemabridge core functionality """

if __package__:
    from .options import Options
    from .prompt import Prompt
else:
    from options import Options
    from prompt import Prompt
import sys

def main():
    """ Main execution thread """

    options = Options().load_options()
    connect_string = "host=" + options["host"] + " port=" + options["port"] + " dbname=" + options["db"] + " user=" + options["username"] + " password=" + options["password"]
    prompt = Prompt(connect_string)
    prompt.prompt = 'schemabridge> '
    prompt.cmdloop('[+] Starting schemabridge interface...')

if __name__ == '__main__':
    sys.exit(main())
