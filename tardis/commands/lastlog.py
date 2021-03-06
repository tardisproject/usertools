from tardis.consts import exit_code
import tardis.ldaptools
from collections import defaultdict

# lastlog - audit users



def setup(parser):
    parser.add_argument("--type", "-t", help="Audit user logins -- abandon for abandonment -- password for password type.")

def command(args):
    ldap = tardis.ldaptools.LDAP()
    ldap.connect()
    userlist = ldap.getUsers()
    print "Found %d users in LDAP currently." %len(userlist)
    if args.type == "abandon" or not args.type:
        print "##### Abandonment audit #####"
        logonHistory = defaultdict(list)
        for user in userlist:
            username = user[-1]["uid"][-1]
            lastSeen = ldap.getLastSeen(username)
            logonHistory[lastSeen].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
        for k, v in logonHistory.iteritems():
            print "%s: %d" %(k, len(v))
        if args.type == "abandon":
            exit(exit_code.SUCCESS)

    if args.type == "password" or not args.type:
        print "##### Password type audit #####"
        passwordTypes = defaultdict(list)
        for user in userlist:
            passwordType = re.findall("^\{(.*?)\}", user[-1]["userPassword"][-1])
            if passwordType:
                passwordTypes[passwordType[0]].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
            elif user[-1]["userPassword"][-1] == "":
                passwordTypes[None].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
            else:
                passwordTypes["plain"].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))

        for k, v in passwordTypes.iteritems():
            print "%s: %d" %(k, len(v))
        exit(exit_code.SUCCESS)

    assert False, "Argument '-t' requires either 'abandon' or 'password'."
    exit(exit_code.ERR_INVALID_ARGS)