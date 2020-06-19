#!/usr/bin/env python3
import sys

filePath = sys.argv[1]
enumItems = False
with open(filePath, 'r') as f:
    for line in f.readlines():
        l = line.strip()
        if enumItems:
            # skip all enum items
            if not l.startswith('-'):
                enumItems = False
                print(line, end='')
        elif l.startswith('enum:'):
            enumItems = True
        elif not l.startswith('pattern:'):
            print(line, end='')
