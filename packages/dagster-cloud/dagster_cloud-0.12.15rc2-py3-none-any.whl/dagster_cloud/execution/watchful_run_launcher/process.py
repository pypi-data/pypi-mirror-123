import os
import subprocess

from dagster.core.launcher.base import LaunchRunContext
from dagster.grpc.types import ExecuteRunArgs
from dagster.serdes.ipc import interrupt_ipc_subprocess_pid
from dagster.serdes.serdes import serialize_dagster_namedtuple

from . import WatchfulRunLauncher

PID_TAG = "process/pid"


class ProcessRunLauncher(WatchfulRunLauncher):
    def launch_run(self, context: LaunchRunContext) -> None:
        run = context.pipeline_run
        pipeline_code_origin = context.pipeline_code_origin

        input_json = serialize_dagster_namedtuple(
            ExecuteRunArgs(
                pipeline_origin=pipeline_code_origin,
                pipeline_run_id=run.run_id,
                instance_ref=self._instance.get_ref(),
            )
        )

        args = ["dagster", "api", "execute_run", input_json]
        process = subprocess.Popen(args)

        self._instance.add_run_tags(run.run_id, {PID_TAG: str(process.pid)})

    def _get_pid(self, run):
        if not run or run.is_finished:
            return None

        tags = run.tags

        if PID_TAG not in tags:
            return None

        return int(tags[PID_TAG])

    def can_terminate(self, run_id):
        run = self._instance.get_run_by_id(run_id)
        if not run:
            return False

        pid = self._get_pid(run)
        if not pid:
            return False

        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def terminate(self, run_id):
        run = self._instance.get_run_by_id(run_id)
        if not run:
            return False

        pid = self._get_pid(run)
        if not pid:
            return False

        self._instance.report_run_canceling(run)

        interrupt_ipc_subprocess_pid(pid)

        return True

    def check_run_health(self, _run_id):
        pass
