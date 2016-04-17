import argparse

from tardis.commands.adduser import setup as adduser_setup, command as adduser_func
from tardis.commands.userinfo import setup as userinfo_setup, command as userinfo_func

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Subcommands', description="TARDIS Project Toolkit")

    # Command: adduser
    # Maintainer: Gareth Pulham <kline@tardis.ed.ac.uk>
    adduser_p = subparsers.add_parser('adduser', description="Create a new user on TARDIS", help="Create a new user on TARDIS")
    adduser_setup(adduser_p)
    adduser_p.set_defaults(func=adduser_func)
    
    # Command: userinfo
    # Maintainer: Gareth Pulham <kline@tardis.ed.ac.uk>
    userinfo_p = subparsers.add_parser('userinfo', description="Search for a user on TARDIS", help="Search for a user on TARDIS")
    userinfo_setup(userinfo_p)
    userinfo_p.set_defaults(func=userinfo_func)


    args = parser.parse_args()
    args.func(args)
