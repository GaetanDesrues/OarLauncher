import subprocess
import sys
from contextlib import redirect_stdout
from functools import partial
from multiprocessing import Pool

from process_args import process_args


def worker(x, out=None, name=None):
    if out:
        # redirect does not work with processes: may do it in runme.sh but oarsub manages logs itself
        with open(out, "w") as f:
            with redirect_stdout(f):
                print(f"Runme args: {x.strip()}")
                # TODO: implement > stdout 2> stderr in subprocess.check_output
                return subprocess.check_output([name, x.strip()]).decode(
                    sys.stdout.encoding
                )
    else:
        return subprocess.check_output([name, x.strip()]).decode(sys.stdout.encoding)


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

        jobids = [1506000 + x for x in range(len(data))]
        print("\n".join([f"JobID: {x}" for x in jobids]))

        out = None
        if job.stdout:
            out = [job.stdout.replace("%jobid%", str(x)) for x in jobids]

        with Pool(int(job.core)) as p:
            print(f"Starting {len(data)} jobs on {job.core} cores")
            p.starmap(partial(worker, name=job.runme), zip(data, out))

    else:
        print(f"Starting 1 job\nJobID: 1506000")

        out = None
        if job.stdout:
            out = job.stdout.replace("%jobid%", "1506000")
        worker(" ".join(job.args), name=job.runme, out=out)


if __name__ == "__main__":
    _job = process_args(sys.argv)

    if _job.script_stdout:
        with open(_job.script_stdout, "w") as f:
            with redirect_stdout(f):
                main(_job)
    else:
        main(_job)
