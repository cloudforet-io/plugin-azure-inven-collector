from spaceone.api.inventory.plugin import job_pb2_grpc, job_pb2
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.service import JobService
import traceback
import logging

_LOGGER = logging.getLogger(__name__)


class Job(BaseAPI, job_pb2_grpc.JobServicer):
    pb2 = job_pb2
    pb2_grpc = job_pb2_grpc

    def get_tasks(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service("JobService", metadata) as job_svc:
            return self.locator.get_info("TasksInfo", job_svc.get_tasks(params))
