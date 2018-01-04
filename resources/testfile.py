#! /usr/bin/python

'''
    Some commentary, just to take up space ...

'''

import os
import sys


things = 'some cool stuff'.split()


def main():
    for thing in things:
        if thing:
            print(thing)
        else:
            print("There is no thing.")


def foo():
    ''' Not implemented.'''
    pass
