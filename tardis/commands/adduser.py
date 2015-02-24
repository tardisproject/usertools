def setup(parser):
    parser.add_argument("username", help="Username for the new user")

def command(args):
    print("TARDIS PROJECT - Create New User Account")
    print("Creating User %s" % (args.username,))
