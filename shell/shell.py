#! /usr/bin/env python3

import sys, os, re


def main():
    while True:
        path = os.getcwd().encode()
        os.write(1, path)
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, (" $ ").encode())

        input = os.read(0, 1000)  # arbitrary number
        input = input.decode().split()

        userInputHandler(input)

        print(input)


def userInputHandler(input):
    if len(input) == 0:
        return
    if input[0].lower() == "exit":
        sys.exit(0)
    elif input[0].lower() == "cd":
        if len(input) > 1:
            try:
                os.chdir(input[1])
            except FileNotFoundError:
                pass
        else:
            os.chdir("..")
    else:  # taken from p3 demo
        pid = os.getpid()
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, input[0])
                try:
                    os.execve(program, input, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

            os.write(2, ("Command not found %s\n" % input[0]).encode())
            sys.exit(1)  # terminate with error
        else:
            os.wait()  # fixes output string timing


if __name__ == "__main__":
    main()
