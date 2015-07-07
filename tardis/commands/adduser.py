import tardis.ldaptools
import logging
import smtplib
import random
import string
import pprint
import os

# adduser - add a user to tardis ldap
# exit codes:
#   0   - Normal
#   100 - Username in use

def setup(parser):
    parser.add_argument("username", help="Username for the new user")

def command(args):
    ldap = tardis.ldaptools.LDAP()
    ldap.connect()

    logging.debug("Getting userlist")
    userlist = ldap.getUsers()
    
    # Check username is available
    logging.debug("Checking username is available")
    if args.username in [user[-1]["uid"][0] for user in userlist]:
        logging.debug("... it's not!")
        print "Username %s is already in use." % args.username
        exit(100)

    # Get lowest available UID
    logging.debug("Getting lowest available UID")
    uidlist = set(range(10000, 60000))   # https://www.debian.org/doc/debian-policy/ch-opersys.html#s9.2.2
    uidlist -= set(int(user[-1]["uidNumber"][0]) for user in userlist)
    lowestuid = sorted(list(uidlist))[0]
    logging.debug("... %d" % lowestuid)

    # Actually build the new user
    password = "".join(random.choice(string.hexdigits) for _ in range(8))
    salt = "".join(chr(random.randint(0, 255)) for _ in range(4))
    newuser = {
        "uidNumber": [str(lowestuid)],
        "objectClass": [
            "account",
            "posixAccount",
            "top",
            "CourierMailAccount",
            "CourierMailAlias",
            "tardisAccount",
            "shadowAccount"
        ],
        "uid": [args.username],
        "loginShell": ["/bin/bash"],
        "quota": ["10000000S"],
        "gidNumber": ["1005"],      # "Student" group
        "userPassword": [tardis.ldaptools.ssha1(password, salt)]
    }

    # Pairs of ldapname, friendlyname we still need to get
    fields = [
        ("gecos", "Full name: "),
        ("homePostalAddress", "Address: "),
        ("homePhone", "Home Telephone: "),
        ("sponsors", "Sponsor: "),
        ("externalEmail", "External EMail: ")
    ]

    for field in fields:
        newuser[field[0]] = [raw_input(field[1])]

    # Extra elements inferred from what we have
    newuser["cn"] = newuser["gecos"]    # Apparently(!)
    newuser["maildrop"] = ["%s/" % args.username]
    newuser["homeDirectory"] = ["/home/%s" % args.username]
    newuser["mail"] = ["%s@tardis.ed.ac.uk" % args.username]
    newuser["mailbox"] = [args.username]    # Kev questioned the need for this in the original script

    # Add their user mapping
    newmap = {
        "cn": ["amdmap amd.home[%s]" % args.username],
        "objectClass": ["amdmap"],
        "amdmapName": ["amd.home"],
        "amdmapKey": [args.username],
        "amdmapValue": ["fs:=/var/autofs/newusers/%s" % args.username]
    }

    # Have the operator confirm
    print "Your new user:"
    pprint.pprint(newuser, width=1)

    confirm = raw_input("Do you wish to create this account? y/n: ")
    if confirm == 'y':
        logging.debug("Adding user")
        ldap.addUser(args.username, newuser)

        logging.debug("Adding map")
        ldap.addMap(args.username, newmap)

        logging.debug("Adding directories")
        # Homedir and symlink
        os.system("mkdir /var/autofs/users/%s" % args.username)
        os.system("ln -s /var/autofs/users/%s /var/autofs/newusers/%s" %(args.username, args.username))

        # Mail
        os.system("maildirmake /var/autofs/mail/%s" % args.username)
        os.system("ln -s /var/autofs/mail/%s /var/autofs/newusers/%s/Maildir" %(args.username, args.username))
        os.system("chown -R %i:1005 /var/autofs/newusers/%s" % (lowestuid, args.username))
        os.system("chown -R %i:1005 /var/autofs/mail/%s" % (lowestuid, args.username))

        # Send welcome mail
        logging.debug("Sending welcome mail")
        mailer = smtplib.SMTP("mail")

        email =  "From: support@tardis.ed.ac.uk\n"
        email += "To: %s\n" % newuser['externalEmail'][0]
        email += "Subject: Your new Tardis account!\n"
        email += "\n"
        email += "%s, your Tardis account has now been created and is\n" % newuser['cn'][0]
        email += "available for login immediately. Details of how to log in to the\n"
        email += "Tardis systems can be found at\n"
        email += "\n"
        email += "http://wiki.tardis.ed.ac.uk/index.php/Shell_Service\n"
        email += "\n"
        email += "Your login details are:\n"
        email += "  Username: %s\n" % newuser["uid"][0]
        email += "  Password: %s\n" % password
        email += "\n"
        email += "You are required to change your password immediately upon first\n"
        email += "login to something memorable. You do not need to retain this\n"
        email += "original password once you have changed it\n"

        mailer.sendmail("support@tardis.ed.ac.uk", [newuser['externalEmail'][0]], email)
        mailer.quit()
        print "Welcome mail sent"

        # Alert sysmans
        logging.debug("Sending mail to sysmans")
        mailer = smtplib.SMTP("mail")

        email =  "From: accounts@tardis.ed.ac.uk\n"
        email += "To: sysmans@tardis.ed.ac.uk\n"
        email += "Subject: New Tardis Account Created\n"
        email += "\n"
        email += "Account Name: %s\n" % newuser["uid"][0]
        email += "Account Holder: %s\n" % newuser['cn'][0]
        email += "External Contact: %s\n" % newuser['externalEmail'][0]
        email += "Sponsor: %s\n" % newuser['sponsors'][0]

        mailer.sendmail("accounts@tardis.ed.ac.uk", "sysmans@tardis.ed.ac.uk", email)
        mailer.quit()
        print "Sysmans informed"
