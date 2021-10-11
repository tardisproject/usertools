# coding=utf-8
import tardis.ldaptools
import logging
import smtplib
import random
import string
import pprint
import os
from subprocess import Popen, PIPE


# resetpw - Reset a user's password
# exit codes:
#   0   - Normal
#   100 - User not found

def setup(parser):
    parser.add_argument("username", help="Username of the user who needs a password reset")

def command(args):
    ldap = tardis.ldaptools.LDAP()
    ldap.connect()
    try:
        user = ldap.getUser(args.username)     
    except:
        print "User %s doesn't exist" % args.username
        exit(100)

    print "Resetting the password for %s \n  username: %s\n  email: %s\n  externalEmail: %s" % (user[-1]['cn'][0], user[-1]['uid'][0], user[-1]['mail'][0], user[-1]['externalEmail'][0] if 'externalEmail' in user[-1] else 'None')
    confirm = raw_input("Do you want to reset %s's password? y/n: " % user[-1]['cn'][0])
    if confirm != 'y':
        print "Operation cancelled"
        exit(0)

    password = "".join(random.choice(string.hexdigits) for _ in range(14))
    salt = "".join(chr(random.randint(0, 255)) for _ in range(4))

    hashedPassword = tardis.ldaptools.ssha1(password, salt)

    ldap.updateUser(args.username, {"userPassword": hashedPassword})
    logging.debug("Sending email notification")
    mailer = smtplib.SMTP("mail")

    email =  "From: support@tardis.ed.ac.uk\n"
    email += "To: %s\n" % user[-1]['externalEmail'][0]
    email += "Subject: 🔑 Tardis Password Reset\n"
    email += "\n"
    email += "%s, your Tardis password has been reset.\n" % user[-1]['cn'][0]
    email += "Details of how to log in to the "
    email += "Tardis systems can be found at\n"
    email += "\n"
    email += "http://wiki.tardis.ed.ac.uk/index.php/Shell_Service\n"
    email += "\n"
    email += "Your login details are:\n"
    email += "  Username: %s\n" % user[-1]["uid"][0]
    email += "  Password: %s\n" % password
    email += "\n"
    email += "Please change your password immediately upon first "
    email += "login to something memorable & secure. You do not need to retain this "
    email += "original password once you have changed it\n"

    mailer.sendmail("support@tardis.ed.ac.uk", [user[-1]['externalEmail'][0]], email)
    mailer.quit()
    print "Email sent to user"

    # Alert sysmans
    logging.debug("Sending mail to sysmans")
    mailer = smtplib.SMTP("mail")
    whoami = Popen(["whoami"], stdout=PIPE)
    username = whoami.communicate()[0].replace("\n", "")
    email =  "From: accounts@tardis.ed.ac.uk\n"
    email += "To: sysmans@tardis.ed.ac.uk\n"
    email += "Subject: 🔑 Tardis Password Reset Notification\n"
    email += "\n"
    email += "The password for %s (username: %s) was reset by %s\n" % (user[-1]["cn"][0], user[-1]["uid"][0], username)
 

    mailer.sendmail("accounts@tardis.ed.ac.uk", "sysmans@tardis.ed.ac.uk", email)
    mailer.quit()
    print "Sysmans informed"
    exit(0)
    