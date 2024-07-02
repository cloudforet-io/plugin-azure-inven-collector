from schematics.models import Model
from schematics.types import ListType, StringType
from schematics.types.compound import ModelType

__all__ = ["Tasks"]


class TaskOptions(Model):
    resource_type = StringType(serialize_when_none=False)
    cloud_service_types = ListType(StringType, serialize_when_none=False)


class Task(Model):
    task_options = ModelType(TaskOptions, required=True)


class Tasks(Model):
    tasks = ListType(ModelType(Task), required=True)
