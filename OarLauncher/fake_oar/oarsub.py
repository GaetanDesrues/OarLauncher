import logging
import subprocess
import sys
from contextlib import redirect_stdout
from functools import partial
from multiprocessing import Pool

from process_args import process_args

log = logging.getLogger(__name__)


def main(job):
    # import prettyprinter as pp
    # pp.install_extras(exclude=["django", "attrs", "ipython_repr_pretty", "ipython"])
    # pp.pprint(job)

    with open(job.runme) as f:
        ct = f.readlines()
    ct = [x for x in ct if not x.startswith("source /etc/profile.d/modules.sh")]
    ct = [x for x in ct if not x.startswith("module load")]
    with open(job.runme, "w") as f:
        f.write(" ".join(ct))

    if job.param_file:
        with open(job.param_file) as f:
            data = f.readlines()

    print(f"Starting {len(data)} jobs")
    print("\n".join([f"JobID: 1512546{x}" for x in range(len(data))]))

    for x in data:
        subprocess.call([job.runme, x.strip()])


if __name__ == "__main__":
    _job = process_args(sys.argv)

    if _job.script_stdout:
        with open(_job.script_stdout, "w") as f:
            with redirect_stdout(f):
                main(_job)
    else:
        main(_job)
