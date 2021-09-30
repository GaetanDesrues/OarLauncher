import logging
import re
from dataclasses import dataclass
from typing import TypeVar

J = TypeVar("J", bound="Job")


def process_args(argv) -> J:
    j = Job()
    # print(argv)
    if len(argv) == 0:
        return j
    elif argv[1] == "sub":
        j.prgm = "oarctl"
        argv = argv[2:]
    else:
        j.prgm = "oarsub"
        argv = argv[1:]
    args = " ".join(argv)
    # print(args)

    m = re.search(r"--resource /host=(\d+)/core=(\d+),walltime=(\d+(:\d+)+)", args)
    j.host = m.group(1)
    j.core = m.group(2)
    j.walltime = m.group(3)

    m = re.search(r"--array-param-file (/?\S+)", args)
    j.param_file = m.group(1)

    m = re.search(r"--stdout (/?\S+)", args)
    j.stdout = m.group(1)

    m = re.search(r"--stderr (/?\S+)", args)
    j.stderr = m.group(1)

    m = re.search(r"--queue (\w+)", args)
    j.queue = m.group(1)

    m = re.search(r"> (/?\S+) 2>?(/?\S+)", args)
    if m:
        j.script_stdout = m.group(1)
        j.script_stderr = m.group(2)
        if j.script_stderr == "&1":
            j.script_stderr = j.script_stdout

    for x in argv[::2]:
        if "--" not in x:
            j.runme = x
            break

    return j


@dataclass
class Job:
    host: int = None
    core: int = None
    walltime: str = None
    queue: str = None
    stdout: str = None
    stderr: str = None
    script_stdout: str = None
    script_stderr: str = None
    runme: str = None
    prgm: str = None
    param_file: str = None


log = logging.getLogger(__name__)
