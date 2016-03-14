__author__ = 'vaioco'

import os

ACCESS_FLAGS = [
    (0x1, 'public'),
    (0x2, 'private'),
    (0x4, 'protected'),
    (0x8, 'static'),
    (0x10, 'final'),
    (0x20, 'synchronized'),
    (0x40, 'bridge'),
    (0x80, 'varargs'),
    (0x100, 'native'),
    (0x200, 'interface'),
    (0x400, 'abstract'),
    (0x800, 'strictfp'),
    (0x1000, 'synthetic'),
    (0x4000, 'enum'),
    (0x8000, 'unused'),
    (0x10000, 'constructor'),
    (0x20000, 'synchronized'),
]


def check_cache(dir,target):
    for root, dirs, files in os.walk(dir):
        if target in files:
            print files
            return True
    return False