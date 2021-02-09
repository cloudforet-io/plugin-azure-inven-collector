from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType
from spaceone.inventory.model.loadbalancer.data import LoadBalancer


class Tags(Model):
    key = StringType()
    value = StringType()


class SqlDatabase(Model):
    name = StringType()
    id = StringType()
    type = StringType()
    subscription_id = StringType()
    subscription_name = StringType()
    resource_group = StringType()
    location = StringType()

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://portal.azure.com/#@.onmicrosoft.com/resource{self.id}/overview",
        }