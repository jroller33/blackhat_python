import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


# receives a cmd, runs it, and returns the output as a string
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    
    # 'check_output' method runs a cmd on the local OS and returns the output from the cmd
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="John's Netcat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
        netcat.py -t 192.168.1.108 -p 5555 -l -c     # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt     # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"    # execute command
        echo 'ABC' | 
    
    '''))