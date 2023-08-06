"""Standard standalone utility functions"""
import os
import subprocess
import signal
import shlex


def run_cmd(cmd, retry=3, timeout=300, success_ret=(0,), use_shell=False):
    """Used to simply run a command"""
    proc = subprocess.Popen(shlex.split(
        cmd), stdout=subprocess.PIPE, shell=use_shell)
    try:
        output = proc.communicate(timeout)[0]
        brc = proc.returncode
    except subprocess.TimeoutExpired:
        # send signal to the process group
        os.killpg(os.getpgid(proc.pid), signal.SIGINT)
        output, brc = None, -1

    if brc not in success_ret and retry > 0:
        output, brc = run_cmd(cmd, retry - 1, timeout, success_ret)
    return output, brc
