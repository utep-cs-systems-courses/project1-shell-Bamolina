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
    elif '|' in input: # If there is a pipe in the input, pass the input to the pipeHandler
        pipeHandler(input)
    else:
        commandHandler(input)

def pipeHandler(input):
    leftInput  = input[0:input.index('|')]
    rightInput = input[input.index('|')+1:]
    # from p5 demo
    pr, pw = os.pipe()
    rc = os.fork()
    if rc < 0:
        sys.exit(1)

    elif rc == 0:  # child - will write to pipe
        os.close(1)  # redirect child's stdout
        os.dup(pw)
        os.set_inheritable(1, True)
        for fd in (pr, pw):
            os.close(fd)
        commandHandler(leftInput)
        sys.exit(1)
    else:  # parent (forked ok)
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0, True)
        for fd in (pw, pr):
            os.close(fd)
        if '|' in rightInput: # Recursive call in case there are multiple pipes
            pipeHandler(rightInput)
        commandHandler(rightInput)
        sys.exit(1)

def redirectHandler(input):
    if '>' in input:
        os.close(1)
        os.open(input[input.index('>')+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        commandHandler(input[0:input.index('>')])
        


    if '<' in input:
        os.close(0)
        os.open(input[input.index('<')+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(0, True)
        commandHandler(input[0:input.index('<')])

def commandHandler(input):
    # taken from p3 demo
    pid = os.getpid()
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        if '>' in input or '<' in input:
            redirectHandler(input)
        else:
            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, input[0])
                try:
                    os.execve(program, input, os.environ)  # try to exec program
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

        os.write(2, ("Command not found: %s\n" % input[0]).encode())
        sys.exit(1)  # terminate with error
    else:
        os.wait()  # fixes output string timing



if __name__ == "__main__":
    main()
