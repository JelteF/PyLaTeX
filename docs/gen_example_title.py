import sys

title = sys.argv[1]

if title.endswith('_ex'):
    title = title[:-3]

title = title.replace('_', ' ')
title = title.capitalize() + ' example'

print(title)
print(len(title) * '=')
