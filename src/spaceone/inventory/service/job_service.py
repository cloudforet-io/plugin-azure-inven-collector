import logging

from spaceone.core.service import *
from spaceone.inventory.model.job_model import Tasks
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class JobService(BaseService):
    resource = "Job"

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(["options", "secret_data"])
    def get_tasks(self, params: dict):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - task_filter
        """

        options = params.get("options", {})
        secret_data = params.get("secret_data", {})

        tasks = []

        cloud_service_types = options.get(
            "cloud_service_types", CLOUD_SERVICE_GROUP_MAP.keys()
        )

        for cloud_service_type in cloud_service_types:
            tasks.append(
                {
                    "task_options": {
                        "cloud_service_types": [cloud_service_type],
                    }
                }
            )
        tasks = Tasks({"tasks": tasks})
        tasks.validate()

        return tasks.to_primitive()
