from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType


class Disk(Model):
    id = StringType()
    name = StringType()
    location = StringType()

    def reference(self):
        return {
            "resource_id": "",
            "external_link": ""
        }
