#!/usr/bin/python
"""Set Psiphon admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import string
import sys
import getopt
import hashlib
import random
import binascii

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

password=""

salt=binascii.hexlify(str(random))
salt = salt[:32]
def _get_hashpass(password):
    hash=hashlib.sha1(password+salt).hexdigest()
    return hash





    
def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Psiphon Password",
            "Enter new password for the Psiphon 'admin' account.")
    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Psiphon Email",
            "Enter email address for the Psiphon 'admin' account.",
            "admin@example.com")

    hashpass=_get_hashpass(password)
    m = MySQL()
    m.execute('UPDATE psiphon.user SET email=\"%s\" WHERE uname=\"admin\";' % email)
    m.execute('UPDATE psiphon.user SET pass=\"%s\" WHERE uname=\"admin\";' % hashpass)
    m.execute('UPDATE psiphon.user SET pass_salt=\"%s\" WHERE uname=\"admin\";' % salt)


if __name__ == "__main__":
    main()

