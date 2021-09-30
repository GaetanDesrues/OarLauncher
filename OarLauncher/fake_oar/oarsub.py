import logging
import re
import sys

import prettyprinter as pp
import treefiles as tf

from process_args import process_args

log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    job = process_args(sys.argv)

    pp.install_extras(exclude=["django", "attrs", "ipython_repr_pretty", "ipython"])
    pp.pprint(job)

    with open(job.runme) as f:
        ct = f.read()

        re.search(r"", ct)

    if job.param_file:
        data = tf.load_txt(job.param_file)

        for x in data:
            print(x)
