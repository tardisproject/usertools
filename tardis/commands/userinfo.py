import tardis.ldaptools
import logging
from subprocess import Popen, PIPE

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
        users = ldap.searchUser("cn", "*"+args.realname+"*")
    elif args.uid:
        users = ldap.searchUser("uidNumber", args.uid)
    else:
        assert False, "ArgParse promises at least one argument but none were non-None?"

    logging.debug("Found %d users" % len(users))
    if users:
        for user in users:
            p1 = Popen(["lastlog", "-u", username], stdout=PIPE)
            p2 = Popen(["grep", "-v", "Latest"], stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()
            output = p2.communicate()[0].replace("\n", "")
            lastSeen = ""
            if output.endswith("**"):
                lastSeen = "Never"
            else:
                lastseen = re.findall("\d{4}$", output)
            groups = ldap.getGroupsForUser(user[-1].get("uid", [None])[0])
            print "Username:", user[-1].get("uid", [None])[0]
            print "UserID:", user[-1].get("uidNumber", [None])[0]
            print "GroupID:", user[-1].get("gidNumber", [None])[0]
            print "Secondary Groups:", ", ".join("%s (%s)" % (group[1]["cn"][0],group[1]["gidNumber"][0]) for group in groups)
            print "Realname:", user[-1].get("cn", [None])[0]
            print "External Email:", user[-1].get("externalEmail", [None])[0]
            print "Sponsor:", user[-1].get("sponsors", [None])[0]
            print "Last Seen:", lastSeen 
            print ""
        exit(0)
    else:
        print "No users found"
        exit(100)

