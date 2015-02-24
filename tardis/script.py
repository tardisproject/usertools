import argparse

from tardis.commands.adduser import setup as adduser_setup, command as adduser_func

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Subcommands', description="TARDIS Project Toolkit")

    # Command: adduser
    # Author: Harry Reeder <skull@tardis.ed.ac.uk>
    adduser_p = subparsers.add_parser('adduser', description="Create a new user on TARDIS", help="Create a new user on TARDIS")
    adduser_setup(adduser_p)
    adduser_p.set_defaults(func=adduser_func)

    args = parser.parse_args()
    args.func(args)
