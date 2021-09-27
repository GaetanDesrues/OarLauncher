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