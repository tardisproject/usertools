from tardis.consts import exit_code
import tardis.ldaptools
import logging

# userinfo - get a users info


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
        users = ldap.searchUser("uid", args.username, includeDisabled=True)
    elif args.realname:
        users = ldap.searchUser("cn", "*"+args.realname+"*", includeDisabled=True)
    elif args.uid:
        users = ldap.searchUser("uidNumber", args.uid, includeDisabled=True)
    else:
        assert False, "ArgParse promises at least one argument but none were non-None?"

    logging.debug("Found %d users" % len(users))
    if users:
        for (cn, user) in users:
            lastSeen = ldap.getLastSeen(args.username)
            groups = ldap.getGroupsForUser(user.get("uid", [None])[0])
            disabled = "DisabledUsers" in cn

            print "Username:", user.get("uid", [None])[0]
            print "UserID:", user.get("uidNumber", [None])[0]
            print "GroupID:", user.get("gidNumber", [None])[0]
            print "Secondary Groups:", ", ".join("%s (%s)" % (group[1]["cn"][0],group[1]["gidNumber"][0]) for group in groups)
            print "Realname:", user.get("cn", [None])[0]
            print "External Email:", user.get("externalEmail", [None])[0]
            print "Sponsor:", user.get("sponsors", [None])[0]
            print "Last Seen:", lastSeen 
            print "Disabled:", disabled
            print ""
        exit(exit_code.SUCCESS)
    else:
        print "No users found"
        exit(exit_code.ERR_USER_NOT_FOUND)

