import tardis.ldaptools
from collections import defaultdict
from subprocess import Popen, PIPE
import re

# lastlog - audit users
# exit codes:
#   0   - Normal
#   100 - audit failed somehow


def setup(parser):
    parser.add_argument("--type", -"t", help="Audit user logins -- abandon for abandonment -- password for password type.")

def command(args):
    ldap.connect()
    userlist = ldap.getUsers()
    print "Found %d users in LDAP currently." %len(userlist)
    if args.type == "abandon" or not args.type:
        print "##### Abandonment audit #####"
        logonHistory = defaultdict(list)
        for user in userlist:
            username = user[-1]["uid"][-1]

            p1 = Popen(["lastlog", "-u", username], stdout=PIPE)
            p2 = Popen(["grep", "-v", "Latest"], stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()
            output = p2.communicate()[0].replace("\n", "")
            if output.endswith("**"):
                logonHistory["never"].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
            else:
                logonHistory[re.findall("\d{4}$", output)[0]].append((user[-1]["uid"][-1], user[-1]["uidNumber"][-1]))
        for k, v in logonHistory.iteritems():
            print "%s: %d" %(k, len(v))
        if args.type == "abandon":
            exit(0)

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
        exit(0)

    if args.type != "abandon" or args.type != "password" or args.type != None: 
        assert False, "Argument '-t' requires either 'abandon' or 'password'."
        exit(100)