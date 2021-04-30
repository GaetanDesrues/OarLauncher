import logging
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List

import treefiles as tf
import treefiles.oar as oar

from OarLauncher.dumpers import dump_exe, dump_data
from OarLauncher.templates import RUNME_SCRIPT, START_OAR, NOTIFY_SCRIPT


class ArrayJob:
    Data = defaultdict(list)

    def __init__(
        self, gen_dir: tf.Tree, data: Dict[str, List[str]], job_path: str = None
    ):
        self.g = gen_dir
        self.data = data
        self.job_path = job_path

        self.setup_files()
        self.nb_jobs = len(next(iter(data.values())))

        self.oar_cmd = None

    def dump(self):
        self.dump_data()
        self.dump_notif_script()
        self.dump_oar_command()
        self.dump_runme()

        log.info(f"Files are dumped to file://{self.g.abs()}")

    def run(self) -> str:
        shell_out = subprocess.check_output(self.g.start_oar)
        shell_out = shell_out.decode("utf-8").strip()
        return shell_out

    def setup_files(self):
        self.g.file(
            "start_oar.sh",
            fifo="pipe_file.fifo",
            notify="notify_exec.sh",
            array="array_args.txt",
            runme="runme.sh",
            oar="oarsub_res.txt",
        )

    def dump_runme(self):
        runme_script = RUNME_SCRIPT.format(
            activate=tf.Tree(sys.executable).p.path("activate"),
            python_job=self.job_path,
        )
        dump_exe(self.g.runme, runme_script)

    def dump_notif_script(self):
        notify_script = NOTIFY_SCRIPT.format(fifo_file=self.g.fifo)
        dump_exe(self.g.notify, notify_script)

    def build_oar_command(self, minutes=1, hours=0, core=1, queue=oar.Queue.BESTEFFORT):
        self.oar_cmd = oar.start_oar(
            self.g.runme,
            logs_dir=self.g.dir("logs").dump(),
            array_fname=self.g.array,
            notify=oar.NotifyOar(self.g.notify).exec,
            do_run=False,
            wall_time=oar.walltime(minutes=minutes, hours=hours),
            core=core,
            queue=queue,
        )

    def dump_oar_command(self,):
        start_oar_script = START_OAR.format(
            oar_command=" ".join(self.oar_cmd),
            fifo_file=self.g.fifo,
            oar_msg_file=self.g.oar,
            nb_jobs=self.nb_jobs,
        )
        dump_exe(self.g.start_oar, start_oar_script)

    def dump_data(self):
        dump_data(self.g.array, self.data)


log = logging.getLogger(__name__)
