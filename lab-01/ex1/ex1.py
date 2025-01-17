#!/usr/bin/env python3

import base64

# You are given a string that has been encoded multiple times.
# Your goal is to repeatedly decode it until you reveal the hidden flag.
# You do not know how many times the text has been encoded.

encoded_text = b'VmxSR1lWUXhTa2hXYWxwV1ZrVkthRlpyVm1GamJHUlhWV3RhVG1FemFGWldWbWhyVjJ4YVNGUnFRbFZoTVVwVFdsZHpOVlpGTVZoaVJuQlhUVVJGZWxaRldtdFVNa3BIWWtoR1YySlhlRTlaVjNSTFlqRmtjMVZzU2s5U1ZFWmFWRlZSZDFCUlBUMD0='
# TODO 1: Decode the string repeatedly until the text is not encoded anymore

# Solution:
decode_1 = base64.b64decode(encoded_text).decode("utf-8")
decode_2 = base64.b64decode(decode_1).decode("utf-8")
decode_3 = base64.b64decode(decode_2).decode("utf-8")
decode_4 = base64.b64decode(decode_3).decode("utf-8")
decode_5 = base64.b64decode(decode_4).decode("utf-8")

decoded_text = decode_5

print("Final decoded text:", decoded_text)
# Result: ISC{44e1da16-40a7-4439-bac0-ceb5b20ae481
