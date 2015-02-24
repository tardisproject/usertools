import argparse

from tardis.commands.adduser import setup as adduser_setup, command as adduser_func

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Subcommands', description="TARDIS Project Toolkit")

    adduser_p = subparsers.add_parser('adduser', description="Create a new user on TARDIS", help="Create a new user on TARDIS")
    adduser_setup(adduser_p)
    adduser_p.set_defaults(func=adduser_func)

    deluser_p = subparsers.add_parser('deluser', description="Delete a user from TARDIS", help="Delete a user from TARDIS")
    deluser_p.add_argument("username", help="User to remove from TARDIS")

    create_p = subparsers.add_parser('create', description="Create an account on a non-LDAP service", help="Create an account on a non-LDAP service")
    create_sp = create_p.add_subparsers(title='Services', description='Non-LDAP Services')

    create_xmpp_p = create_sp.add_parser('xmpp', description="Create your XMPP account", help="Create your XMPP account")

    create_sip_p = create_sp.add_parser('sip', description="Create your SIP account", help="Create your SIP account")
    create_sip_p.add_argument

    args = parser.parse_args()
    args.func(args)
