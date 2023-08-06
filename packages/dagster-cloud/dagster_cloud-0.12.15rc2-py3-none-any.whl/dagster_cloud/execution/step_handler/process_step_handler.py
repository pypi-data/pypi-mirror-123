import subprocess
from collections import defaultdict
from typing import Dict, List
from dagster.core.definitions.event_metadata import EventMetadataEntry

from dagster.core.events import DagsterEvent, DagsterEventType, EngineEventData
from dagster.core.executor.step_delegating import StepHandler
from dagster.core.executor.step_delegating.step_handler.base import StepHandlerContext
from dagster.serdes import serialize_dagster_namedtuple
from dagster.serdes.ipc import interrupt_ipc_subprocess_pid
import threading


class ProcessStepHandler(StepHandler):
    def __init__(self) -> None:
        super().__init__()
        self._step_pids: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._step_pids_lock = threading.Lock()

    @property
    def name(self) -> str:
        return "ProcessStepHandler"

    def launch_step(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        assert (
            len(step_handler_context.execute_step_args.step_keys_to_execute) == 1
        ), "Launching multiple steps is not currently supported"
        step_key = step_handler_context.execute_step_args.step_keys_to_execute[0]

        input_json = serialize_dagster_namedtuple(step_handler_context.execute_step_args)
        args = ["dagster", "api", "execute_step", input_json]
        p = subprocess.Popen(args)

        with self._step_pids_lock:
            self._step_pids[step_handler_context.execute_step_args.pipeline_run_id][
                step_key
            ] = p.pid
        return []

    def check_step_health(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        # TODO not implemented
        return []

    def terminate_step(self, step_handler_context: StepHandlerContext) -> List[DagsterEvent]:
        assert (
            len(step_handler_context.execute_step_args.step_keys_to_execute) == 1
        ), "Launching multiple steps is not currently supported"
        step_key = step_handler_context.execute_step_args.step_keys_to_execute[0]

        with self._step_pids_lock:
            pid = self._step_pids[step_handler_context.execute_step_args.pipeline_run_id][step_key]

        events = [
            DagsterEvent(
                event_type_value=DagsterEventType.ENGINE_EVENT.value,
                pipeline_name=step_handler_context.execute_step_args.pipeline_origin.pipeline_name,
                step_key=step_key,
                message="Stopping process for step",
                event_specific_data=EngineEventData(
                    [
                        EventMetadataEntry.text(step_key, "Step key"),
                        EventMetadataEntry.int(pid, "Process id"),
                    ],
                ),
            )
        ]
        interrupt_ipc_subprocess_pid(pid)
        return events
