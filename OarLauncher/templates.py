START_OAR = """
#!/bin/bash

{oar_command}
""".strip()

RUNME_SCRIPT = """
#!/bin/bash

source /etc/profile.d/modules.sh
module load conda/2020.11-python3.8

source {activate}
{python_path}
python {python_job} "$@"
""".strip()
