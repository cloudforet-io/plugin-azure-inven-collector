__all__ = ["TasksInfo", "TaskInfo"]

import functools
from spaceone.api.inventory.plugin import job_pb2
from spaceone.core.pygrpc.message_type import *


def TaskInfo(task_data):
    info = {"task_options": change_struct_type(task_data["task_options"])}
    return job_pb2.TaskInfo(**info)


def TasksInfo(result, **kwargs):
    tasks_data = result.get("tasks", [])

    return job_pb2.TasksInfo(
        tasks=list(map(functools.partial(TaskInfo, **kwargs), tasks_data)),
    )
