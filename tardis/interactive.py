import argparse

from tardis.commands.adduser import setup as adduser_setup, command as adduser_func
from tardis.commands.userinfo import setup as userinfo_setup, command as userinfo_func
from tardis.commands.lastlog import setup as lastlog_setup, command as lastlog_func

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

    # Command: userinfo
    # Maintainer: Maya Copeland <maya@tardis.ed.ac.uk>
    lastlog_p = subparsers.add_parser('lastlog', description="Read through TARDIS logs", help="Search through tardis logs via their login security or their last login")
    lastlog_setup(lastlog_p)
    lastlog_p.set_defaults(func=lastlog_func)

    args = parser.parse_args()
    args.func(args)
