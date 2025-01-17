#!/usr/bin/python3

import grp
import hashlib
import os
import pyotp
import sys


PASSWORD_HASH = "13412ffd6149204f40e546ffa9fbd7124b410198a6ba3924f788622b929c8eb2"
TOTP_SECRET = "TODO" # TODO(7.1): Choose a secret!


def login():
    user = os.environ.get("PAM_USER")

    user_groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]

    # TODO(6.1): We want this script to be used only for our special group of users.

    user_secret = input()
    user_password = user_secret

    # TODO(7.2): Extract the password and the TOTP. Hint: you know the length of the TOTP.

    # TODO(6.2): Calculate the hash of the provided password.

    if user_hash != PASSWORD_HASH:
        print("Ai gresit buzunarul!")
        return False

    # TODO(7.3): Check the TOTP from the user and uncomment the code below.

#    if not totp_correct:
#        print("S-a rezolvat, nu se poate!")
#        return False

    print("Ma distrez si bine fac!")
    return True


if __name__ == "__main__":
    sys.tracebacklimit = 0

    if not login():
        raise Exception("Python script rejected login: trying default authentication")
