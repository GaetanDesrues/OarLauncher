import logging
import subprocess
import sys
from typing import Dict, List

import treefiles as tf

from OarLauncher.dumpers import dump_exe, dump_data
from OarLauncher.templates import RUNME_SCRIPT, START_OAR


class ArrayJob:
    # Data = defaultdict(list)  # directly use `defaultdict(list)`

    def __init__(
        self, gen_dir: tf.Tree, data: Dict[str, List[str]], job_path: str = None
    ):
        self.g = gen_dir
        self.data = data
        self.job_path = job_path

        self.setup_files()
        self.nb_jobs = len(next(iter(data.values())))

        self.oar_cmd = None

    def dump(self, activate: str = None, python_path: List[str] = None, **envs):
        python_path = tf.none(python_path, [])
        python_path = [f"\nexport PYTHONPATH=$PYTHONPATH:{x}" for x in python_path]
        for k, v in envs.items():
            python_path.append(f"\nexport {k}={v}")

        self.dump_data()
        self.dump_runme(activate=activate, python_path="".join(python_path))

        log.info(f"Files are dumped to file://{self.g.abs()}")

    def run(self) -> str:
        shell_out = subprocess.check_output(self.g.start_oar)
        shell_out = shell_out.decode("utf-8").strip()
        return shell_out  # empty except if `stdout` argument of tf.start_oar is set to None

    def setup_files(self):
        self.g.file(
            start_oar="start_oar.sh",
            array="array_args.txt",
            runme="runme.sh",
            oar="oarsub_res.txt",
        )

    def dump_runme(self, python_path: str, activate: str = None):
        act = tf.none(activate, tf.curDirs(sys.executable, "activate"))
        runme_script = RUNME_SCRIPT.format(
            activate=act,
            python_job=self.job_path,
            python_path=python_path,
        )
        dump_exe(self.g.runme, runme_script)

    def build_oar_command(
        self,
        to_file: bool = True,
        **kwargs,
    ):
        stdout = self.g.oar if to_file else None
        self.oar_cmd = tf.start_oar(
            self.g.runme,
            # prgm=tf.Program.OARCTL,
            logs_dir=self.g.dir("logs").dump(),
            array_fname=self.g.array,
            do_run=False,
            stdout=stdout,  # if None, output of oarsub in returned in <ArrayJob.run>
            **kwargs,
        )

        oar_command = START_OAR.format(oar_command=" ".join(self.oar_cmd))
        dump_exe(self.g.start_oar, oar_command)

    def dump_data(self):
        dump_data(self.g.array, self.data)


log = logging.getLogger(__name__)
