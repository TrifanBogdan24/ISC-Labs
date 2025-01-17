#!/bin/bash

# ✅

find /usr/include/ -mindepth 1 -maxdepth 2 -type d -exec du -sh {} + | sort -h
