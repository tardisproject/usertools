import tardis.ldaptools
import logging

# userinfo - get a users info
# exit codes:
#   0   - Normal
#   100 - No user found

def setup(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--username", help="Username to search for")
    group.add_argument("-r", "--realname", help="Real name to search for")
    group.add_argument("-i", "--uid", help="Numeric UID to search for")

def command(args):
    logging.debug("Connecting to LDAP")
    ldap = tardis.ldaptools.LDAP()
    ldap.connect()

    logging.debug("Searching...")
    users = []
    if args.username:
        users = ldap.searchUser("uid", args.username)
    elif args.realname:
        print "Realname searches are not currently implemented"
        exit(-1)
    elif args.uid:
        print "UID searches are not currently implemented"
        exit(-1)
    else:
        assert False, "ArgParse promises at least one argument but none were non-None?"

    logging.debug("Found %d users" % len(users))
    if users:
        for user in users:
            print "Username:", user[-1]["uid"][0]
            print "UserID:", user[-1]["uidNumber"][0]
            print "Realname:", user[-1]["cn"][0]
            print "External Email:", user[-1]["externalEmail"][0]
            print "Sponsor:", user[-1]["sponsors"][0]
        exit(0)
    else:
        print "No users found"
        exit(100)

