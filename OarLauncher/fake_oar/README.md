# Simulating oarsub to debug

```bash
sudo nano /usr/local/bin/oarsub
sudo chmod +x /usr/local/bin/oarsub
sudo ln -s /usr/local/bin/oarsub /usr/local/bin/oarctl
```

In `/usr/local/bin/oarsub`:
```bash
#!/bin/bash

source <path-to>/venv/bin/activate

python <path-to>/OarLauncher/fake_oar/oarsub.py "$@"
```

### To test

Launch this script:
```python
out_dir = tf.Tree.new(__file__, "generated").dump(clean=True)

nb_jobs, data = 2, defaultdict(list)
for i in range(nb_jobs):
    data["simu_dir"].append(f"d_{i}")
    data["infos"].append(f"this is job {i}")

job_script = tf.curDirs(__file__, "my_fake_job.py")

jobs = ArrayJob(out_dir, data, job_script)
jobs.build_oar_command(
    wall_time=tf.walltime(minutes=2),
    prgm=tf.Program.OARSUB,
)
jobs.dump()
jobs.run()
```

In `my_fake_job.py`:
```python
args = json.loads(sys.argv[1])
log.info(f"Received {args}")
```