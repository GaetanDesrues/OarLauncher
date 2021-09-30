import logging
from collections import defaultdict

import treefiles as tf

from OarLauncher.array_job import ArrayJob


def main():
    # Choose directory where script and logs are dumped
    out_dir = tf.fTree(__file__, "generated").dump(clean=True)

    # Create the parameters array
    nb_jobs, data = 10, defaultdict(list)
    for i in range(nb_jobs):
        data["simu_dir"].append(f"d_{i}")
        data["infos"].append(f"this is job {i}")

    # Path of the script that will be called by each job of the array
    # Each line of data will be sent to this script as json command line argument
    job_script = tf.curDirs(__file__, "job.py")

    # Create the job array
    jobs = ArrayJob(out_dir, data, job_script)
    # Build the command line that will be sent to shell
    jobs.build_oar_command(
        queue=tf.Queue.BESTEFFORT,
        to_file=True,  # whereas `shell_out` is dumped to file or returned via command line
        wall_time=tf.walltime(minutes=2),
        prgm=tf.Program.OARCTL,  # `OARCTL` is blocking (main process is running until all jobs end), `OARSUB` is not
    )
    # Generate and write scripts and ressource files
    jobs.dump(
        # python_path=[...],  # you can give a list of python paths that will be added to PYTHONPATH
        # MY_ENV=...,  # you can also specify PATH envs by passing them as kwargs
    )

    # Start the job array
    log.info(f"Starting jobs, check `oarstat -u`")
    shell_out = jobs.run()  # blocking operation if prgm=tf.Program.OARCTL
    log.info(shell_out)

    log.debug("Resuming program")


log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()

    main()
