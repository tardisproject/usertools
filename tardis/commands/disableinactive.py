from tardis.consts import exit_code
import tardis.ldaptools
from collections import defaultdict

# disableinactive - disable users that haven't logged in since a certain year



def setup(parser):
    parser.add_argument("threshold", type=int, help="Users who have not logged in on or before this year are disabled")
    parser.add_argument("-n", "--disable-never", action="store_true", help="Users who have never logged in are disabled")

def command(args):
    if "threshold" not in args:
        assert False, "threshold is a required argument"
        exit(exit_code.ERR_INVALID_ARGS)
    
    ldap = tardis.ldaptools.LDAP()
    ldap.connect()
    userlist = ldap.getUsers()
    print "Found %d users in LDAP currently." % len(userlist)
    
    logonHistory = defaultdict(list)
    for user in userlist:
        username = user[-1]["uid"][-1]
        lastSeen = ldap.getLastSeen(username)
        logonHistory[lastSeen].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
    
    keysToDisable = []
    for k in logonHistory.keys():
        if (k == "Never" and args.disable_never) or (k != "**" and int(k) <= args.threshold):
            keysToDisable.append(k)
    
    allUsers = []
    print "To disable:"
    for k in keysToDisable:
        print("\t%s" % k)
        for v in logonHistory[k]:
            print("\t\t%s" % str(v))
            allUsers.append(v)

    print "Enter 'YES' to continue"
    if raw_input() != 'YES':
        assert False, "Operation Aborted"
        exit(exit_code.ERR_UNKNOWN_ERROR)

    for (username, _) in allUsers:
        print "Disabling %s" % username
        ldap.disableUser(username)

    exit(exit_code.SUCCESS)