#! /usr/bin/env python3

import sys, os, re


def main():
    while True:

        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())

        input = os.read(0,1000)
        input = input.split()
        print(input)


if __name__ == "__main__":
    main()