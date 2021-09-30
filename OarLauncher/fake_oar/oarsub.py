import logging
import subprocess
import sys

# import prettyprinter as pp
from functools import partial
from multiprocessing import Pool

import treefiles as tf

from process_args import process_args

log = logging.getLogger(__name__)


def start_job(x, job=None):
    return subprocess.call([job, x.strip()])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    job = process_args(sys.argv)

    # pp.install_extras(exclude=["django", "attrs", "ipython_repr_pretty", "ipython"])
    # pp.pprint(job)

    with open(job.runme) as f:
        ct = f.readlines()
    ct = [x for x in ct if not x.startswith("source /etc/profile.d/modules.sh")]
    ct = [x for x in ct if not x.startswith("module load")]
    # print(ct)
    with open(job.runme, "w") as f:
        f.write(" ".join(ct))

    if job.param_file:
        with open(job.param_file) as f:
            data = f.readlines()

    with Pool(len(data)) as p:
        res = p.map(partial(start_job, job=job.runme), data)

    print(res)
