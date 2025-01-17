#!/usr/bin/python3

import pyotp
import pyqrcode


TOTP_SECRET = "TODO" # TODO(1): Choose a secret!

totp_auth = pyotp.totp.TOTP(TOTP_SECRET).provisioning_uri(
    name="Nicolae Guta", issuer_name="Lab ISC"
)

# TODO(2): Generate and display the setup QR code.
