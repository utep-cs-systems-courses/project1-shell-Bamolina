#! /usr/bin/env python3

import sys, os, re


def main():
    while True:

        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())

        input = os.read(0,1000)
        input = input.decode().split()

        userInputHandler(input)

        print(input)

def userInputHandler(input):
    if input[0].lower() == "exit":
        return;
    elif input[0].lower() == "cd":
        if len(input) > 1:
            try:
                os.chdir(input[1])
            except FileNotFoundError:
                pass
        else:
            os.chdir("..")


if __name__ == "__main__":
    main()