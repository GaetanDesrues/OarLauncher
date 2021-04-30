START_OAR = """
#!/bin/bash

if [ -f {fifo_file} ]; then
    rm {fifo_file}
fi
mkfifo {fifo_file}

{oar_command} > {oar_msg_file} 2>&1

NB_JOBS=0
while [ $NB_JOBS -lt {nb_jobs} ]; do
    read REPLY
    (( NB_JOBS++ ))
done <> {fifo_file}

echo "$NB_JOBS jobs done! Last reply: $REPLY"
""".strip()


NOTIFY_SCRIPT = """
#!/bin/bash

echo "$*" > {fifo_file}
""".strip()


RUNME_SCRIPT = """
#!/bin/bash

source /etc/profile.d/modules.sh
module load conda/2020.11-python3.8

source {activate}

python {python_job} $1
""".strip()
