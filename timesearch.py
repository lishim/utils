#!/bin/python

import os
import sys
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', help='file containing sequential data')
parser.add_argument('range_from', help='beginning of search range, inclusive')
parser.add_argument('range_to', help='end of search range, exclusive')
parser.add_argument('-r', '--regex', type=str, help='match specified regex only')
args = parser.parse_args()

# regex examples:
#   ./timesearch.py request.log "26/Nov/2015:12:59:19" "26/Nov/2015:12:59:20" -r "(?<= \- \- \[).*"

FILE_NAME= args.file
STR_FROM = args.range_from
STR_TO = args.range_to

if STR_FROM >= STR_TO:
  print 'ERROR: range_from >= range_to'
  sys.exit(1)

if args.regex:
  REGEX = re.compile(args.regex)
else:
  REGEX = None

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
  if REGEX:
    match = REGEX.search(line)
    if match is None:
      print 'line ' + line + ' does not match regex ' + REGEX.pattern
      sys.exit(1)
    else:
      line = match.group(0)
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
  if REGEX:
    match = REGEX.search(line)
    if match is None:
      print 'line ' + line + ' does not match regex ' + REGEX.pattern
      sys.exit(1)
    else:
      line = match.group(0)
  if STR_TO >= line:
    i = mid
  else:
    j = mid

SEEK_TO = j

f.seek(SEEK_FROM)
while f.tell() < SEEK_TO:
  print f.readline(),
