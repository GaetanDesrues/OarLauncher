import logging

import treefiles as tf

from OarLauncher.array_job import ArrayJob


def main():
    # Choose directory where script and logs are dumped
    out_dir = tf.Tree.new(__file__, "generated").dump(clean=True)

    # Create parameters array
    nb_jobs, data = 10, ArrayJob.Data
    for i in range(nb_jobs):
        data["simu_dir"].append(f"d_{i}")
        data["infos"].append(f"this is job {i}")

    # Path of the script that will be called by each job of the array
    # Each line of data will be sent to this script as json command line argument
    job_script = tf.curDirs(__file__, "job.py")

    # Create the job array
    jobs = ArrayJob(out_dir, data, job_script)
    # Setup jobs conf
    jobs.build_oar_command(minutes=1, queue=tf.oar.Queue.BESTEFFORT)
    # Write scripts
    jobs.dump()
    # Start the job array
    shell_out = jobs.run()  # blocking operation
    log.info(shell_out)

    log.debug("Resuming program")


log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger()
    # log = tf.get_logger(default=False, handlers=[tf.stream_csv_handler()])

    main()
