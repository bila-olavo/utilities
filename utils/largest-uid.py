#!/usr/bin/python

maxuid = 0
for line in open ("/etc/passwd"):
    split = line.split(":")
    if int(split[2]) > maxuid:
        maxuid = int(split[2])
print(maxuid)