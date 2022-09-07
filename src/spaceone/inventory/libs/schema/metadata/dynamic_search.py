from schematics import Model
from schematics.types import StringType, ListType, PolyModelType


class BaseDynamicSearch(Model):
    name = StringType()
    key = StringType()
    data_type = StringType(choices=['string', 'integer', 'float', 'boolean', 'datetime'],
                           serialize_when_none=False)


class BaseDynamicSearchItem(Model):
    title = StringType(default="Properties")
    items = ListType(PolyModelType(BaseDynamicSearch), serialize_when_none=False)
