### Simply start oar job array on nef cluster

**NB**: To simply start a stand-alone job, use [`treefiles.start_oar`](https://github.com/GaetanDesrues/TreeFiles/blob/master/treefiles/oar.py#L64-L178).


#### Install
```bash
pip install --upgrade OarLauncher
```


#### Usage
```python
from collections import defaultdict
import treefiles as tf
from OarLauncher import ArrayJob


# Choose a directory where script and logs are dumped
out_dir = tf.Tree.new(__file__, "generated").dump(clean=True)

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
# Setup jobs conf
jobs.build_oar_command(
    queue=tf.Queue.BESTEFFORT,
    to_file=True,  # whereas `shell_out` is dumped to file or returned via command line
    wall_time=tf.walltime(minutes=2),
    prgm=tf.Program.OARCTL,  # `OARCTL` is blocking (main process is running until all jobs end), `OARSUB` is not
)
# Write scripts
jobs.dump(
    # python_path=[...],  # you can give a list of python paths that will be added to PYTHONPATH
    # MY_ENV=...,  # you can also specify PATH envs by passing them as kwargs
)
# Start the job array
shell_out = jobs.run()  # blocking operation if prgm=tf.Program.OARCTL
print(shell_out)
```

## `tf.start_oar`

```python
def start_oar(
    runme_str,
    logs_dir: Union[tf.Tree, str] = None,
    array_fname: str = None,
    wall_time: str = walltime(minutes=1),
    host: int = 1,
    core: int = 1,
    job_name: str = None,
    queue: str = Queue.DEFAULT,
    cmd_fname: str = None,
    runme_args: List[str] = None,
    do_run: bool = True,
    with_json: bool = False,
    notify: List = None,
    prgm: str = Program.OARSUB,
    stdout: str = None,
    stderr: str = None,
) -> Union[str, List[str]]:
    """
    Builds an oar command.
    Usage example:
    .. code::
            cdir = tf.Tree.new(__file__)
            sdir = cdir.dir("OarOut").dump(clean=True)
            res = start_oar(
                runme_str=cdir.path("runme.sh"),
                logs_dir=sdir,
                walltime=time(minute=10),
                queue="besteffort",
                core=2,
                cmd_fname=sdir.path("cmd.sh"),
                do_run=True,
            )
    :param runme_str: path to the runme script or command line
    :param logs_dir: directory for std out/err
    :param array_fname: path to the arguments file (array file)
    :param wall_time: wall time of the job
    :param host: numbre of nodes
    :param core: number of cores
    :param job_name: job name
    :param queue: job queue ['default', 'besteffort']
    :param cmd_fname: path to a file to save the oar command
    :param runme_args: list of command line arguments given to the runme script
    :param do_run: whether to execute the command or not
    :param with_json: add the -J option in oarsub command
    :param notify: notify options [List], you may use the class NotifyOar to build this option
    :param prgm: `oarsub` or `oarctl sub`
    :param stdout: path for stdout
    :param stderr: path for stderr, defaults to stdout if None
    :return: The output of the oar command if `do_run` is True else the oar command
    """
```