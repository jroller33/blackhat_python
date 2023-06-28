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