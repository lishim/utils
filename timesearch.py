#!/bin/python

import os
import sys

FILE_NAME= sys.argv[1]
STR_FROM = sys.argv[2]
STR_TO = sys.argv[3]

file_size = os.stat(FILE_NAME).st_size
if file_size == 0:
  sys.exit()

f=open(FILE_NAME)

# find beginning of range
i=0
j=file_size-1
x=0
while True:
  x += 1
  if x == 1000:
    print 'ERROR: too many iterations'
    sys.exit(1)
  mid = (i + j) / 2
  # seek to the middle
  f.seek(mid)
  # read up to the next newline
  f.readline()
  # advance mid to start of line
  mid = f.tell()
  if mid >= j:
    break
  line = f.readline()
  if STR_FROM <= line:
    j = mid
  else:
    i = mid

SEEK_FROM = j

# find end of range
i=0
j=file_size-1
x=0
while True:
  x += 1
  if x == 1000:
    print 'ERROR: too many iterations'
    sys.exit(1)
  mid = (i + j) / 2
  # seek to the middle
  f.seek(mid)
  # read up to the next newline
  f.readline()
  # advance mid to start of line
  mid = f.tell()
  if mid >= j:
    break
  line = f.readline()
  if STR_TO >= line:
    i = mid
  else:
    j = mid

SEEK_TO = j

f.seek(SEEK_FROM)
while f.tell() < SEEK_TO:
  print f.readline(),

