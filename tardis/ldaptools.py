import ConfigParser
import ldap

import hashlib
import base64
import re
from subprocess import Popen, PIPE

def ssha1(password, salt):
    """
    This is the hash function used by OpenLDAP+pam_ldap.
    It expects a password of any length, and a four (4) byte salt
    """
    phash = hashlib.sha1()
    phash.update(password)
    phash.update(salt)
    return "{SSHA}" + base64.b64encode(phash.digest() + salt)

class LDAP(object):
    def __init__(self, configFile="/etc/tardis/ldap.conf"):
        config = ConfigParser.SafeConfigParser()
        config.readfp(open(configFile, 'r'))

        for option in ("hostname", "binddn", "bindpw", "base"):
            try:
                setattr(self, option, config.get("server", option))
            except ConfigParser.NoOptionError:
                setattr(self, option, None)

    def connect(self, hostname="", binddn="", bindpw=""):
        if hostname: self.hostname = hostname
        if binddn: self.binddn = binddn
        if bindpw: self.bindpw = bindpw

        self.conn = ldap.open(self.hostname)
        self.conn.simple_bind_s(self.binddn, self.bindpw)
    
    # User management
    def searchUser(self, field, value, includeDisabled=False):
        results = self.conn.search_s("ou=People, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="%s=%s" % (field, value))
        if includeDisabled and len(results) == 0:
            results += self.conn.search_s("ou=DisabledUsers, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="%s=%s" % (field, value))
        return results

    def getUser(self, username):
        results = self.conn.search_s("ou=People, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="uid=%s" % username)
        return results[0]

    def getUsers(self):
        results = self.conn.search_s("ou=People, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="uid=*")
        return results
    
    def addUser(self, username, details):
        updates = [(key, value) for key, value in details.iteritems()]
        self.conn.add_s('uid=%s, ou=People, %s' %(username, self.base), updates)
        
    def updateUser(self, username, details):
        # Example: [
        #               (ldap.MOD_REPLACE, "gecos", "Joe Bloggs"),
        #               (ldap.MOD_REPLACE, "homePhone", "123 456")
        #          ]
        # will update username's gecos and homePhone with the above values.
        # Pass in the keys and values as a dictionary.
        updates = [(ldap.MOD_REPLACE, key, value) for key, value in details.iteritems()]
        self.conn.modify_s('uid=%s, ou=People, %s' %(username, self.base), updates)

    def disableUser(self, username):
        self.conn.rename_s("uid=%s,ou=People,%s" % (username, self.base), "uid=%s" % username, "ou=DisabledUsers,%s" % self.base)

    def getLastSeen(self, username):
        p1 = Popen(["lastlog", "-u", username], stdout=PIPE)
        p2 = Popen(["grep", "-v", "Latest"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        output = p2.communicate()[0].replace("\n", "")
        lastSeen = ""
        if output.endswith("**"):
            return "Never"
        else:
            lastSeen = re.findall("\d{4}$", output)
            return lastSeen[0] if lastSeen else "???"

    def deleteUser(self, username):
        self.conn.delete('uid=%s, ou=People, %s' %(username, self.base))

    # Group management
    def getGroupsForUser(self, username):
        results = self.conn.search_s("ou=Group, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="memberUid=%s" % username)
        return results

    def getGroup(self, groupname):
        results = self.conn.search_s("ou=Group, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="cn=%s" % groupname)
        return results[0]

    def getGroups(self):
        results = self.conn.search_s("ou=Group, %s" %self.base, ldap.SCOPE_SUBTREE, filterstr="cn=*")
        return results

    def addGroup(self, groupname, details):
        updates = [(key, value) for key, value in details.iteritems()]
        self.conn.add_s('cn=%s, ou=Group, %s' %(groupname, self.base), updates)

    def updateGroup(self, groupname, details):
        updates = [(ldap.MOD_REPLACE, key, value) for key, value in details.iteritems()]
        self.conn.modify_s('cn=%s, ou=Group, %s' %(groupname, self.base), updates)

    def deleteGroup(self, groupname):
        self.conn.delete('cn=%s, ou=Group, %s' %(groupname, self.base))

    # Map management
    def getMap(self, mapname):
        results = self.conn.search_s(
            "ou=Maps, %s" %self.base,
            ldap.SCOPE_SUBTREE,
            filterstr="cn=amdmap amd.home[%s]" %mapname
        )
        return results[0]

    def getMaps(self, mapname):
        results = self.conn.search_s(
            "ou=Maps, %s" %self.base,
            ldap.SCOPE_SUBTREE,
            filterstr="cn=*" %mapname
        )
        return results

    def addMap(self, mapname, details):
        updates = [(key, value) for key, value in details.iteritems()]
        self.conn.add_s('cn=amdmap amd.home[%s], ou=Maps, %s' %(mapname, self.base), updates)

    def updateMap(self, mapname, details):
        updates = [(ldap.MOD_REPLACE, key, value) for key, value in details.iteritems()]
        self.conn.modify_s('cn=amdmap amd.home[%s], ou=Maps, %s' %(mapname, self.base), updates)

    def deleteMap(self, mapname):
        self.conn.delete_s("cn=amdmap amd.home[%s], ou=Maps, %s" %(mapname, self.base))
